from flask import Blueprint, request, jsonify
import logging
from src.database import db, Patient, Message
from src.services.openai_service import OpenAIService
from src.services.evolution_service import EvolutionService

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/evolution', methods=['POST'])
def evolution_webhook():
    """
    Recebe os webhooks enviados pela Evolution API.
    Processa especificamente o evento 'messages.upsert'.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON payload provided"}), 400

    event = data.get("event")
    instance = data.get("instance")
    
    # Processa apenas eventos de nova mensagem inserida
    if event == "messages.upsert":
        message_data = data.get("data", {})
        key = message_data.get("key", {})
        from_me = key.get("fromMe", False)
        remote_jid = key.get("remoteJid", "")
        
        # Filtra o número limpo do remetente
        phone = remote_jid.split('@')[0]
        if not phone:
            return jsonify({"status": "ignored", "reason": "No JID found"}), 200

        # Captura o texto da mensagem a partir dos possíveis campos do protocolo whatsapp
        message_content = ""
        message_payload = message_data.get("message", {})
        
        if "conversation" in message_payload:
            message_content = message_payload["conversation"]
        elif "extendedTextMessage" in message_payload:
            message_content = message_payload["extendedTextMessage"].get("text", "")
        elif "imageMessage" in message_payload:
            message_content = "[Imagem recebida]"
        elif "audioMessage" in message_payload:
            message_content = "[Áudio recebido]"

        if not message_content:
            return jsonify({"status": "ignored", "reason": "Empty message body"}), 200

        # Se a mensagem partiu da própria clínica (celular ou painel)
        if from_me:
            # Rastreia e loga no CRM como mensagem do atendente humano
            patient = Patient.query.filter_by(phone=phone).first()
            if patient:
                # Evita duplicar logs se já inserido pelo endpoint manual do CRM
                existing = Message.query.filter_by(
                    patient_id=patient.id, 
                    content=message_content, 
                    sender='recepcao'
                ).order_by(Message.created_at.desc()).first()
                
                # Se não houver registro recente ou for antigo, loga
                if not existing:
                    agent_msg = Message(patient_id=patient.id, sender='recepcao', content=message_content)
                    db.session.add(agent_msg)
                    db.session.commit()
            return jsonify({"status": "logged_outbound"}), 200

        # Se for mensagem recebida do lead/paciente
        # Executa o processamento do Concierge Digital (IA)
        ai_reply = OpenAIService.process_message(phone, message_content)
        
        if ai_reply:
            # Despacha o texto gerado de volta para o cliente via Evolution API
            success = EvolutionService.send_message(phone, ai_reply)
            return jsonify({"status": "processed", "replied": success}), 200
        else:
            return jsonify({"status": "processed", "replied": False, "reason": "AI disabled (handoff active)"}), 200

    return jsonify({"status": "received", "event": event}), 200
