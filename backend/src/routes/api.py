from flask import Blueprint, request, jsonify
import requests
from src.database import db, Patient, Message, Procedure, Appointment, Doctor, DoctorAvailability, SystemSettings
from src.services.evolution_service import EvolutionService
from src.config import Config
from datetime import datetime, timedelta
from functools import wraps

api_bp = Blueprint('api', __name__)

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Token não fornecido"}), 401
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({"error": "Formato de token inválido"}), 401
            
        token = parts[1]
        if token != "unic_secure_admin_session_token":
            return jsonify({"error": "Token inválido ou expirado"}), 401
            
        return f(*args, **kwargs)
    return decorated

# --- AUTH ENDPOINTS ---

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    
    if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
        return jsonify({"success": True, "token": "unic_secure_admin_session_token"}), 200
        
    return jsonify({"error": "Usuário ou senha incorretos"}), 401

# --- LEADS ENDPOINTS ---

@api_bp.route('/leads', methods=['GET'])
@require_auth
def get_leads():
    """
    Retorna a lista de todos os leads/pacientes cadastrados com suas últimas mensagens.
    """
    patients = Patient.query.order_by(Patient.updated_at.desc()).all()
    results = []
    
    for p in patients:
        lead_dict = p.to_dict()
        
        # Buscar última mensagem
        last_msg = Message.query.filter_by(patient_id=p.id).order_by(Message.created_at.desc()).first()
        if last_msg:
            lead_dict['last_message'] = {
                'content': last_msg.content,
                'created_at': last_msg.created_at.isoformat()
            }
        else:
            lead_dict['last_message'] = None
            
        results.append(lead_dict)
        
    return jsonify(results), 200

@api_bp.route('/leads/<int:lead_id>', methods=['PATCH'])
@require_auth
def update_lead(lead_id):
    """
    Atualiza o nome, a etapa do Kanban ou o status de handoff da IA para um lead.
    """
    patient = Patient.query.get(lead_id)
    if not patient:
        return jsonify({"error": "Lead não encontrado"}), 404
        
    data = request.get_json() or {}
    
    if 'name' in data:
        patient.name = data['name']
    if 'kanban_stage' in data:
        patient.kanban_stage = data['kanban_stage']
    if 'ai_enabled' in data:
        patient.ai_enabled = data['ai_enabled']
        
    db.session.commit()
    return jsonify({"success": True, "lead": patient.to_dict()}), 200


# --- CHAT / MESSAGES ENDPOINTS ---

@api_bp.route('/leads/<int:lead_id>/messages', methods=['GET'])
@require_auth
def get_messages(lead_id):
    """
    Retorna o histórico de mensagens de uma conversa.
    """
    patient = Patient.query.get(lead_id)
    if not patient:
        return jsonify({"error": "Lead não encontrado"}), 404
        
    messages = Message.query.filter_by(patient_id=patient.id).order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

@api_bp.route('/leads/<int:lead_id>/messages', methods=['POST'])
@require_auth
def send_manual_message(lead_id):
    """
    Envia uma mensagem manual do agente (recepção) para o paciente.
    Isso ativa o handoff (pausa a IA: ai_enabled=False).
    """
    patient = Patient.query.get(lead_id)
    if not patient:
        return jsonify({"error": "Lead não encontrado"}), 404
        
    data = request.get_json() or {}
    content = data.get('content')
    if not content:
        return jsonify({"error": "O campo content é obrigatório"}), 400
        
    # Salvar mensagem manual no banco
    msg = Message(patient_id=patient.id, sender='recepcao', content=content)
    db.session.add(msg)
    
    # Pausar a IA (Handoff ativo)
    patient.ai_enabled = False
    db.session.commit()
    
    # Despachar mensagem de verdade para o WhatsApp do cliente
    sent = EvolutionService.send_message(patient.phone, content)
    
    return jsonify({"success": True, "message": msg.to_dict(), "sent_via_whatsapp": sent}), 201


# --- APPOINTMENTS & PROCEDURES ENDPOINTS ---

@api_bp.route('/appointments', methods=['GET'])
@require_auth
def get_appointments():
    """
    Retorna a lista de agendamentos no calendário.
    """
    appointments = Appointment.query.filter_by(status='confirmado').order_by(Appointment.start_time.asc()).all()
    results = []
    
    for appt in appointments:
        patient = Patient.query.get(appt.patient_id)
        procedure = Procedure.query.get(appt.procedure_id)
        
        results.append({
            "id": appt.id,
            "patient": patient.to_dict() if patient else None,
            "procedure": procedure.to_dict() if procedure else None,
            "start_time": appt.start_time.isoformat(),
            "end_time": appt.end_time.isoformat(),
            "status": appt.status
        })
        
    return jsonify(results), 200

@api_bp.route('/appointments', methods=['POST'])
@require_auth
def create_appointment():
    """
    Cria manualmente um agendamento pela recepção.
    """
    data = request.get_json() or {}
    patient_id = data.get('patient_id')
    procedure_id = data.get('procedure_id')
    start_time_str = data.get('start_time') # formato YYYY-MM-DDTHH:MM (ou similar)
    
    if not all([patient_id, procedure_id, start_time_str]):
        return jsonify({"error": "Campos obrigatórios: patient_id, procedure_id, start_time"}), 400
        
    procedure = Procedure.query.get(procedure_id)
    if not procedure:
        return jsonify({"error": "Procedimento não encontrado"}), 404
        
    try:
        # Suporta formatos ISO com ou sem Z/segundos
        start_time_str_cleaned = start_time_str.split('.')[0].replace('Z', '')
        if 'T' in start_time_str_cleaned:
            start_time = datetime.strptime(start_time_str_cleaned, "%Y-%m-%dT%H:%M:%S" if len(start_time_str_cleaned) > 16 else "%Y-%m-%dT%H:%M")
        else:
            start_time = datetime.strptime(start_time_str_cleaned, "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD HH:MM ou formato ISO."}), 400
        
    end_time = start_time + timedelta(minutes=procedure.duration_minutes)
    
    # Validar se o horário está disponível (bloqueio de reserva dupla)
    conflict = Appointment.query.filter(
        Appointment.status == 'confirmado',
        Appointment.start_time < end_time,
        Appointment.end_time > start_time
    ).first()
    
    if conflict:
        return jsonify({"error": "Este horário entra em conflito com outro agendamento ativo."}), 409
        
    appt = Appointment(
        patient_id=patient_id,
        procedure_id=procedure_id,
        start_time=start_time,
        end_time=end_time,
        status='confirmado'
    )
    
    # Se agendado com sucesso, altera a etapa do Kanban do paciente
    patient = Patient.query.get(patient_id)
    if patient:
        patient.kanban_stage = 'agendado'
        
    db.session.add(appt)
    db.session.commit()
    
    return jsonify({"success": True, "appointment": appt.to_dict()}), 201

@api_bp.route('/procedures', methods=['GET'])
@require_auth
def get_procedures():
    """
    Retorna o catálogo de procedimentos cadastrados.
    """
    procedures = Procedure.query.order_by(Procedure.name.asc()).all()
    return jsonify([p.to_dict() for p in procedures]), 200

# --- DOCTORS & AVAILABILITY ENDPOINTS ---

@api_bp.route('/doctors', methods=['GET'])
@require_auth
def get_doctors():
    doctors = Doctor.query.order_by(Doctor.name.asc()).all()
    return jsonify([d.to_dict() for d in doctors]), 200

@api_bp.route('/doctors', methods=['POST'])
@require_auth
def create_doctor():
    data = request.get_json() or {}
    name = data.get('name')
    specialty = data.get('specialty')
    
    if not name or not specialty:
        return jsonify({"error": "Nome e Especialidade são obrigatórios."}), 400
        
    doc = Doctor(name=name, specialty=specialty)
    db.session.add(doc)
    db.session.commit()
    
    # Initialize default schedule for this doctor (Monday-Friday 09:00-18:00)
    for day in range(5): # 0 to 4 (Monday to Friday)
        avail = DoctorAvailability(doctor_id=doc.id, day_of_week=day, start_time="09:00", end_time="18:00")
        db.session.add(avail)
    db.session.commit()
    
    return jsonify({"success": True, "doctor": doc.to_dict()}), 201

@api_bp.route('/doctors/<int:doctor_id>', methods=['DELETE'])
@require_auth
def delete_doctor(doctor_id):
    doc = Doctor.query.get(doctor_id)
    if not doc:
        return jsonify({"error": "Médico não encontrado."}), 404
        
    db.session.delete(doc)
    db.session.commit()
    return jsonify({"success": True}), 200

@api_bp.route('/doctors/<int:doctor_id>/availability', methods=['GET'])
@require_auth
def get_doctor_availability(doctor_id):
    doc = Doctor.query.get(doctor_id)
    if not doc:
        return jsonify({"error": "Médico não encontrado."}), 404
        
    availabilities = DoctorAvailability.query.filter_by(doctor_id=doctor_id).order_by(DoctorAvailability.day_of_week.asc()).all()
    return jsonify([a.to_dict() for a in availabilities]), 200

@api_bp.route('/doctors/<int:doctor_id>/availability', methods=['POST'])
@require_auth
def update_doctor_availability(doctor_id):
    doc = Doctor.query.get(doctor_id)
    if not doc:
        return jsonify({"error": "Médico não encontrado."}), 404
        
    data = request.get_json() or [] # list of availabilities
    # Delete existing availabilities for this doctor
    DoctorAvailability.query.filter_by(doctor_id=doctor_id).delete()
    
    # Add new ones
    for item in data:
        day = item.get('day_of_week')
        start = item.get('start_time', '09:00')
        end = item.get('end_time', '18:00')
        
        if day is not None:
            avail = DoctorAvailability(doctor_id=doctor_id, day_of_week=day, start_time=start, end_time=end)
            db.session.add(avail)
            
    db.session.commit()
    return jsonify({"success": True}), 200

# --- PROCEDURES MANAGEMENT ENDPOINTS ---

@api_bp.route('/procedures', methods=['POST'])
@require_auth
def create_procedure():
    data = request.get_json() or {}
    name = data.get('name')
    description = data.get('description')
    duration_minutes = data.get('duration_minutes')
    price = data.get('price')
    
    if not name or duration_minutes is None or price is None:
        return jsonify({"error": "Nome, Duração (minutos) e Preço são obrigatórios."}), 400
        
    try:
        duration_minutes = int(duration_minutes)
        price = float(price)
    except ValueError:
        return jsonify({"error": "Duração e Preço devem ser numéricos."}), 400
        
    proc = Procedure(name=name, description=description, duration_minutes=duration_minutes, price=price)
    db.session.add(proc)
    db.session.commit()
    
    return jsonify({"success": True, "procedure": proc.to_dict()}), 201

@api_bp.route('/procedures/<int:procedure_id>', methods=['PUT'])
@require_auth
def update_procedure(procedure_id):
    proc = Procedure.query.get(procedure_id)
    if not proc:
        return jsonify({"error": "Procedimento não encontrado."}), 404
        
    data = request.get_json() or {}
    name = data.get('name')
    description = data.get('description')
    duration_minutes = data.get('duration_minutes')
    price = data.get('price')
    
    if name:
        proc.name = name
    if description is not None:
        proc.description = description
    if duration_minutes is not None:
        try:
            proc.duration_minutes = int(duration_minutes)
        except ValueError:
            return jsonify({"error": "Duração deve ser um número inteiro."}), 400
    if price is not None:
        try:
            proc.price = float(price)
        except ValueError:
            return jsonify({"error": "Preço deve ser um número."}), 400
            
    db.session.commit()
    return jsonify({"success": True, "procedure": proc.to_dict()}), 200

@api_bp.route('/procedures/<int:procedure_id>', methods=['DELETE'])
@require_auth
def delete_procedure(procedure_id):
    proc = Procedure.query.get(procedure_id)
    if not proc:
        return jsonify({"error": "Procedimento não encontrado."}), 404
        
    try:
        db.session.delete(proc)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Não é possível excluir este procedimento pois existem agendamentos associados a ele."}), 409
        
    return jsonify({"success": True}), 200

# --- WHATSAPP / EVOLUTION API INTEGRATION ENDPOINTS ---

@api_bp.route('/whatsapp/status', methods=['GET'])
@require_auth
def get_whatsapp_status():
    status = EvolutionService.get_connection_state()
    return jsonify({
        "status": status,
        "instance_name": Config.EVOLUTION_INSTANCE_NAME,
        "is_mock": EvolutionService.is_mock_enabled()
    }), 200

@api_bp.route('/whatsapp/connect', methods=['GET'])
@require_auth
def get_whatsapp_connect():
    status = EvolutionService.get_connection_state()
    if status == "open":
        return jsonify({"status": "open", "message": "Instância já conectada."}), 200
        
    qrcode = EvolutionService.get_qrcode()
    if not qrcode:
        return jsonify({"error": "Não foi possível obter o QR Code da Evolution API."}), 500
        
    return jsonify({
        "status": "connecting",
        "qrcode": qrcode
    }), 200

@api_bp.route('/whatsapp/logout', methods=['POST'])
@require_auth
def post_whatsapp_logout():
    success = EvolutionService.logout()
    if not success:
        return jsonify({"error": "Falha ao desconectar a instância."}), 500
    return jsonify({"success": True}), 200

# --- SYSTEM SETTINGS ENDPOINTS ---

@api_bp.route('/settings', methods=['GET'])
@require_auth
def get_settings():
    settings = SystemSettings.query.first()
    if not settings:
        settings = SystemSettings(
            beta_mode_enabled=True,
            beta_allowed_numbers="",
            auto_activate_ai_for_new_leads=False
        )
        db.session.add(settings)
        db.session.commit()
    return jsonify(settings.to_dict()), 200

@api_bp.route('/settings', methods=['POST'])
@require_auth
def update_settings():
    settings = SystemSettings.query.first()
    if not settings:
        settings = SystemSettings()
        db.session.add(settings)
        
    data = request.get_json() or {}
    
    if 'beta_mode_enabled' in data:
        settings.beta_mode_enabled = bool(data['beta_mode_enabled'])
    if 'beta_allowed_numbers' in data:
        settings.beta_allowed_numbers = str(data['beta_allowed_numbers'])
    if 'auto_activate_ai_for_new_leads' in data:
        settings.auto_activate_ai_for_new_leads = bool(data['auto_activate_ai_for_new_leads'])
        
    # Read clinic institutional profile fields
    if 'clinic_name' in data:
        settings.clinic_name = str(data['clinic_name'])
    if 'clinic_address' in data:
        settings.clinic_address = str(data['clinic_address'])
    if 'clinic_phones' in data:
        settings.clinic_phones = str(data['clinic_phones'])
    if 'clinic_instagram' in data:
        settings.clinic_instagram = str(data['clinic_instagram'])
    if 'clinic_responsible' in data:
        settings.clinic_responsible = str(data['clinic_responsible'])
    if 'clinic_working_hours' in data:
        settings.clinic_working_hours = str(data['clinic_working_hours'])
    if 'clinic_custom_notes' in data:
        settings.clinic_custom_notes = str(data['clinic_custom_notes'])
        
    db.session.commit()
    return jsonify({"success": True, "settings": settings.to_dict()}), 200

# --- WHATSAPP CHAT HISTORY IMPORT ENDPOINTS ---

@api_bp.route('/whatsapp/chats', methods=['GET'])
@require_auth
def get_whatsapp_chats():
    if EvolutionService.is_mock_enabled():
        mock_chats = [
            {"phone": "5512999999999", "name": "Dr. Murillo (Diretor Unic)", "unread": 2},
            {"phone": "5512988888888", "name": "Esposa / Família", "unread": 0},
            {"phone": "5512977777777", "name": "Amanda Cunha (Estética Teste)", "unread": 0},
            {"phone": "5512966666666", "name": "Fornecedor de Equipamento", "unread": 5}
        ]
        
        parsed = []
        for chat in mock_chats:
            patient = Patient.query.filter_by(phone=chat["phone"]).first()
            parsed.append({
                "phone": chat["phone"],
                "name": chat["name"],
                "unread": chat["unread"],
                "already_exists": patient is not None and not patient.ignored,
                "ignored": patient is not None and patient.ignored
            })
        return jsonify(parsed), 200

    url = f"{Config.EVOLUTION_API_URL}/chat/findChats/{Config.EVOLUTION_INSTANCE_NAME}"
    headers = {
        "apikey": Config.EVOLUTION_API_KEY
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            chats_list = response.json() or []
            parsed = []
            for chat in chats_list:
                jid = chat.get("id", "")
                if jid.endswith("@g.us"):
                    continue
                    
                phone = jid.split("@")[0]
                if not phone:
                    continue
                    
                name = chat.get("name") or chat.get("pushName") or "Contato Sem Nome"
                unread = chat.get("unreadCount", 0)
                
                patient = Patient.query.filter_by(phone=phone).first()
                parsed.append({
                    "phone": phone,
                    "name": name,
                    "unread": unread,
                    "already_exists": patient is not None and not patient.ignored,
                    "ignored": patient is not None and patient.ignored
                })
            return jsonify(parsed), 200
        else:
            return jsonify({"error": "Falha ao obter chats da Evolution API."}), 500
    except Exception as e:
        return jsonify({"error": f"Erro de conexão com Evolution API: {str(e)}"}), 500

@api_bp.route('/whatsapp/import-chat', methods=['POST'])
@require_auth
def import_whatsapp_chat():
    data = request.get_json() or {}
    phone = data.get("phone")
    name = data.get("name", "Contato Importado")
    stage = data.get("kanban_stage", "lead_novo")
    
    if not phone:
        return jsonify({"error": "Número do telefone é obrigatório."}), 400
        
    patient = Patient.query.filter_by(phone=phone).first()
    if patient:
        patient.name = name
        patient.kanban_stage = stage
        patient.ignored = False
        patient.is_imported = True
        patient.ai_enabled = False
    else:
        patient = Patient(
            phone=phone,
            name=name,
            kanban_stage=stage,
            is_imported=True,
            ignored=False,
            ai_enabled=False
        )
        db.session.add(patient)
        
    db.session.commit()
    return jsonify({"success": True, "patient": patient.to_dict()}), 200

@api_bp.route('/whatsapp/ignore-chat', methods=['POST'])
@require_auth
def ignore_whatsapp_chat():
    data = request.get_json() or {}
    phone = data.get("phone")
    
    if not phone:
        return jsonify({"error": "Número de telefone é obrigatório."}), 400
        
    patient = Patient.query.filter_by(phone=phone).first()
    if patient:
        patient.ignored = True
        patient.ai_enabled = False
    else:
        patient = Patient(
            phone=phone,
            name="Ignorado",
            kanban_stage="perdido",
            ignored=True,
            ai_enabled=False
        )
        db.session.add(patient)
        
    db.session.commit()
    return jsonify({"success": True}), 200
