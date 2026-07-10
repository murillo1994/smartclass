from flask import Blueprint, request, jsonify
from src.database import db, Patient, Message, Procedure, Appointment
from src.services.evolution_service import EvolutionService
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__)

# --- LEADS ENDPOINTS ---

@api_bp.route('/leads', methods=['GET'])
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
def get_procedures():
    """
    Retorna o catálogo de procedimentos cadastrados.
    """
    procedures = Procedure.query.order_by(Procedure.name.asc()).all()
    return jsonify([p.to_dict() for p in procedures]), 200
