import os
import json
import logging
from datetime import datetime, timedelta
from openai import OpenAI
from src.config import Config
from src.database import db, Patient, Procedure, Appointment, Message, SystemSettings

# Initialize OpenAI client only if key is available
client = None
if Config.OPENAI_API_KEY and "your_openai" not in Config.OPENAI_API_KEY:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Contexto da Unic Clinic - Persona da IA
SYSTEM_PROMPT = """Você é o Concierge Digital da Unic Clinic, uma renomada clínica de estética de alto padrão (boutique).
Seu objetivo principal é atender os clientes no WhatsApp de forma extremamente elegante, educada, solícita e sofisticada.
Guie o lead pelo funil de vendas, tirando dúvidas sobre procedimentos, quebrando objeções e, principalmente, incentivando-o a agendar uma consulta.

Instruções importantes:
1. Responda em Português de forma elegante, clara e sem jargões excessivos.
2. Se o cliente demonstrar interesse em agendar, verifique os procedimentos usando a ferramenta correspondente, mostre as opções de horários disponíveis e realize a reserva de forma integrada.
3. Colete o nome do cliente educadamente se você ainda não souber.
4. Mantenha as respostas concisas e adequadas ao WhatsApp (evite textos longos demais, use quebras de linha para facilitar a leitura).
5. Seja empático e transmita exclusividade.
6. Gerencie ativamente a classificação do lead no funil de vendas (Kanban) chamando a ferramenta correspondente:
   - Chame 'update_lead_stage' com o valor 'qualificacao' assim que você souber o nome do paciente e o procedimento que ele tem interesse.
   - Chame 'update_lead_stage' com o valor 'agendamento_pendente' quando ele demonstrar interesse explícito em agendar e pedir por disponibilidade de dias/horários livres.
   - Chame 'update_lead_stage' com o valor 'perdido' se ele disser que não quer mais nada, achar caro ou recusar o atendimento educadamente.
   (Nota: O estágio 'agendado' é definido automaticamente no banco de dados quando você chama 'book_appointment', então não precisa atualizá-lo manualmente para 'agendado').
"""

# Tool definitions for OpenAI Function Calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_procedures",
            "description": "Retorna o catálogo de procedimentos estéticos oferecidos pela clínica com preços e durações.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_available_slots",
            "description": "Verifica os horários de agendamento disponíveis para um dia específico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "A data no formato YYYY-MM-DD (ex: 2026-07-15)."
                    }
                },
                "required": ["date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Efetua o agendamento de um procedimento estético para um paciente em um dia e horário específicos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "Nome completo do paciente."
                    },
                    "procedure_id": {
                        "type": "integer",
                        "description": "ID do procedimento a ser agendado."
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Data e hora de início no formato YYYY-MM-DD HH:MM (ex: 2026-07-15 14:30)."
                    }
                },
                "required": ["patient_name", "procedure_id", "start_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_lead_stage",
            "description": "Atualiza a etapa do funil de vendas (Kanban) para o cliente correspondente com base no progresso da conversa.",
            "parameters": {
                "type": "object",
                "properties": {
                    "stage": {
                        "type": "string",
                        "enum": ["qualificacao", "agendamento_pendente", "perdido"],
                        "description": "A nova etapa do funil: 'qualificacao' (se souber o nome e procedimento de interesse), 'agendamento_pendente' (se o cliente demonstrar claro interesse em agendar e pedir horários livres), ou 'perdido' (se o cliente recusar/desistir)."
                    }
                },
                "required": ["stage"]
            }
        }
    }
]

# Database Tool Implementations
def get_procedures_db():
    procedures = Procedure.query.all()
    return [p.to_dict() for p in procedures]

def check_available_slots_db(date_str):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return {"error": "Formato de data inválido. Use YYYY-MM-DD."}

    # Grade de horários padrão da clínica: 09:00 às 18:00, de 30 em 30 minutos
    slots = []
    current_time = datetime.combine(target_date, datetime.strptime("09:00", "%H:%M").time())
    end_working_time = datetime.combine(target_date, datetime.strptime("18:00", "%H:%M").time())

    while current_time < end_working_time:
        slots.append(current_time)
        current_time += timedelta(minutes=30)

    # Buscar agendamentos existentes confirmados para essa data
    appointments = Appointment.query.filter(
        db.func.date(Appointment.start_time) == target_date,
        Appointment.status == 'confirmado'
    ).all()

    # Filtrar horários ocupados
    available_slots = []
    for slot in slots:
        occupied = False
        for appt in appointments:
            # Verifica se o horário do slot conflita com a duração do agendamento
            if appt.start_time <= slot < appt.end_time:
                occupied = True
                break
        if not occupied:
            available_slots.append(slot.strftime("%H:%M"))

    return {
        "date": date_str,
        "available_slots": available_slots
    }

def book_appointment_db(phone, patient_name, procedure_id, start_time_str):
    try:
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return {"error": "Formato de data/hora inválido. Use YYYY-MM-DD HH:MM."}

    # Buscar procedimento
    procedure = Procedure.query.get(procedure_id)
    if not procedure:
        return {"error": "Procedimento não encontrado."}

    end_time = start_time + timedelta(minutes=procedure.duration_minutes)

    # Validar se o horário está disponível (bloqueio de reserva dupla)
    conflict = Appointment.query.filter(
        Appointment.status == 'confirmado',
        Appointment.start_time < end_time,
        Appointment.end_time > start_time
    ).first()

    if conflict:
        return {"error": "Desculpe, este horário já foi reservado por outro paciente."}

    # Buscar ou criar paciente
    patient = Patient.query.filter_by(phone=phone).first()
    if not patient:
        patient = Patient(phone=phone, name=patient_name, kanban_stage='agendado')
        db.session.add(patient)
    else:
        if patient_name:
            patient.name = patient_name
        patient.kanban_stage = 'agendado'

    db.session.flush() # obter ID do paciente se for novo

    # Criar agendamento
    appt = Appointment(
        patient_id=patient.id,
        procedure_id=procedure.id,
        start_time=start_time,
        end_time=end_time,
        status='confirmado'
    )
    db.session.add(appt)
    db.session.commit()

    return {
        "success": True,
        "appointment_id": appt.id,
        "patient_name": patient.name,
        "procedure_name": procedure.name,
        "start_time": start_time.strftime("%d/%m/%Y às %H:%M"),
        "message": f"Agendamento de {procedure.name} confirmado com sucesso para {patient.name} em {start_time.strftime('%d/%m/%Y às %H:%M')}!"
    }


class OpenAIService:
    @staticmethod
    def process_message(patient_phone, message_text):
        """
        Processa a mensagem do paciente usando GPT com Function Calling e insere histórico.
        """
        # 1. Obter ou Criar paciente com validação de Whitelist e Configurações Globais
        settings = SystemSettings.query.first()
        if not settings:
            settings = SystemSettings(
                beta_mode_enabled=True,
                beta_allowed_numbers="",
                auto_activate_ai_for_new_leads=False
            )
            db.session.add(settings)
            db.session.commit()

        # Verifica se o número está na whitelist de testes
        is_allowed = False
        if settings.beta_allowed_numbers:
            allowed_list = [num.strip() for num in settings.beta_allowed_numbers.split(",") if num.strip()]
            clean_phone = "".join(filter(str.isdigit, patient_phone))
            for allowed in allowed_list:
                clean_allowed = "".join(filter(str.isdigit, allowed))
                if clean_allowed and (clean_allowed in clean_phone or clean_phone in clean_allowed):
                    is_allowed = True
                    break
        
        # Decide se a IA iniciará ativa
        default_ai_enabled = True
        
        # Se estiver em modo beta e não for número de teste, força IA desativada (humano)
        if settings.beta_mode_enabled and not is_allowed:
            default_ai_enabled = False
        # Se a ativação automática estiver desativada para novos leads
        elif not settings.auto_activate_ai_for_new_leads:
            default_ai_enabled = False

        patient = Patient.query.filter_by(phone=patient_phone).first()
        if not patient:
            patient = Patient(phone=patient_phone, kanban_stage='lead_novo', ai_enabled=default_ai_enabled)
            db.session.add(patient)
            db.session.commit()
        else:
            if settings.beta_mode_enabled and not is_allowed:
                patient.ai_enabled = False
                db.session.commit()

        # Salvar a mensagem do paciente no banco de dados
        user_msg = Message(patient_id=patient.id, sender='paciente', content=message_text)
        db.session.add(user_msg)
        db.session.commit()

        # Caso a IA esteja pausada (handoff ativo), ignoramos o processamento automático
        if not patient.ai_enabled:
            logging.info(f"IA pausada (handoff/modo beta ativo) para o telefone {patient_phone}. Ignorando resposta automática.")
            return None

        # Mock de resposta caso a API key não esteja disponível
        if not client:
            fallback_reply = "Olá! Obrigado por entrar em contato com a Unic Clinic. No momento estou operando em modo offline de demonstração. Em breve um de nossos consultores falará com você."
            ai_msg = Message(patient_id=patient.id, sender='bot', content=fallback_reply)
            db.session.add(ai_msg)
            db.session.commit()
            return fallback_reply

        try:
            # 2. Resgatar as últimas 15 mensagens para histórico de contexto
            past_messages = Message.query.filter_by(patient_id=patient.id).order_by(Message.created_at.asc()).limit(15).all()
            messages_history = [{"role": "system", "content": SYSTEM_PROMPT}]

            for msg in past_messages:
                role = "assistant" if msg.sender == 'bot' else "user"
                # Mensagens do atendente humano (recepcao) agem como contexto de assistente para a IA prosseguir
                if msg.sender == 'recepcao':
                    role = "assistant"
                messages_history.append({"role": role, "content": msg.content})

            # Adicionar a mensagem recém-enviada
            messages_history.append({"role": "user", "content": message_text})

            # Chamada principal à API OpenAI com Tools
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_history,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.7
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            # Loop para resolver Function Calling se solicitado pela LLM
            if tool_calls:
                # Adiciona a resposta inicial da LLM com a requisição da ferramenta ao histórico
                messages_history.append(response_message)

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Executa a função local de banco
                    if function_name == "get_procedures":
                        tool_result = get_procedures_db()
                    elif function_name == "check_available_slots":
                        tool_result = check_available_slots_db(function_args.get("date"))
                    elif function_name == "book_appointment":
                        tool_result = book_appointment_db(
                            phone=patient_phone,
                            patient_name=function_args.get("patient_name"),
                            procedure_id=function_args.get("procedure_id"),
                            start_time_str=function_args.get("start_time")
                        )
                        # Atualiza o nome do paciente no banco local se obtido
                        if "success" in tool_result and function_args.get("patient_name"):
                            patient.name = function_args.get("patient_name")
                            db.session.commit()
                    elif function_name == "update_lead_stage":
                        stage = function_args.get("stage")
                        patient.kanban_stage = stage
                        db.session.commit()
                        tool_result = {"success": True, "stage": stage}
                    else:
                        tool_result = {"error": f"Função {function_name} desconhecida."}

                    # Envia o resultado de volta para o histórico da LLM
                    messages_history.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(tool_result)
                    })

                # Segunda chamada para gerar a resposta final com o contexto das funções
                second_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages_history
                )
                final_text = second_response.choices[0].message.content
            else:
                final_text = response_message.content

            # 3. Salvar resposta da IA no histórico de mensagens
            ai_msg = Message(patient_id=patient.id, sender='bot', content=final_text)
            db.session.add(ai_msg)
            db.session.commit()
            return final_text

        except Exception as e:
            logging.error(f"Erro ao processar mensagem com a OpenAI: {e}")
            fallback_error = "Desculpe, estamos com uma instabilidade técnica. Um atendente humano irá continuar seu atendimento em instantes."
            ai_msg = Message(patient_id=patient.id, sender='bot', content=fallback_error)
            db.session.add(ai_msg)
            db.session.commit()
            return fallback_error
