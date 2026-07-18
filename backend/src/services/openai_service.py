import os
import json
import logging
from datetime import datetime, timedelta
from openai import OpenAI
from src.config import Config
from src.database import db, Patient, Procedure, Appointment, Message, SystemSettings, Doctor

# Initialize OpenAI client only if key is available
client = None
if Config.OPENAI_API_KEY and "your_openai" not in Config.OPENAI_API_KEY:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Contexto da Unic Clinic - Persona da IA (Concierge de Luxo)
SYSTEM_PROMPT = """Você é o Concierge Digital da Unic Clinic, uma renomada clínica de estética de alto padrão (boutique).
Seu objetivo principal é atender os clientes no WhatsApp de forma extremamente elegante, educada, solícita e sofisticada.
Guie o lead pelo funil de vendas, tirando dúvidas sobre procedimentos e quebrando objeções para convencê-lo a agendar uma consulta.

Instruções fundamentais:
1. DIRETRIZES DE ESCRITA:
   - Responda em Português de forma elegante, clara e sem jargões médicos excessivos.
   - Mantenha as respostas concisas e adequadas ao WhatsApp (evite textos longos demais, use quebras de linha para facilitar a leitura).
   - Use NO MÁXIMO 1 emoji por mensagem (ex: ✨ ou 🌸) para manter o visual limpo e refinado.
   - Nunca use gírias ou abreviações (ex: vc, tb).

2. ISOLAMENTO DE VALORES (REGRA DE PREÇO):
   - Você NÃO fala de valores, preços, orçamentos ou formas de pagamento em hipótese alguma.
   - Se o cliente perguntar o preço de qualquer procedimento (ex: "Quanto custa o Botox?"), você deve explicar elegantemente que os valores exatos são definidos de forma personalizada durante a avaliação presencial pelas especialistas, pois cada paciente possui características e indicações únicas. Direcione o cliente a solicitar um agendamento de avaliação física.

3. AGENDAMENTO E TRANSBORDO HUMANO (HANDOFF):
   - O agendamento real e escolha de horários são feitos pela recepção humana.
   - Quando o cliente demonstrar claro interesse em agendar, marcar uma consulta, ou fechar negócio, você deve coletar o nome do cliente educadamente (se ainda não souber) e chamar a ferramenta 'request_appointment'.
   - Após chamar 'request_appointment', explique de forma muito polida que a solicitação foi encaminhada e que uma de nossas atendentes humanas da recepção assumirá a conversa imediatamente para escolher o melhor horário com o cliente.

4. PROFISSIONAIS DA CLÍNICA (MÉDICOS):
   - Se perguntarem sobre os profissionais ou especialistas da clínica, chame a ferramenta 'get_doctors' para informar os nomes e especialidades corretos.

5. HORÁRIO DE ATENDIMENTO:
   - O horário de atendimento oficial da clínica é de Segunda a Sexta, das 09:00 às 18:00.
"""

# Tool definitions for OpenAI Function Calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_procedures",
            "description": "Retorna o catálogo de procedimentos estéticos oferecidos pela clínica com descrições e durações aproximadas (sem valores).",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_doctors",
            "description": "Retorna a lista de médicos, especialistas e profissionais ativos na clínica com suas respectivas especialidades.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "request_appointment",
            "description": "Aciona o transbordo para o atendimento humano na recepção para realizar o agendamento de um procedimento/consulta física.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_name": {
                        "type": "string",
                        "description": "Nome completo do paciente."
                    },
                    "procedure_name": {
                        "type": "string",
                        "description": "Nome do procedimento estético de interesse."
                    },
                    "doctor_name": {
                        "type": "string",
                        "description": "Nome do médico/especialista preferido pelo paciente, se citado."
                    },
                    "preferred_time": {
                        "type": "string",
                        "description": "Data, horário ou período de preferência indicado pelo paciente (ex: 'próxima terça à tarde')."
                    }
                },
                "required": ["patient_name", "procedure_name"]
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
                        "enum": ["qualificacao", "perdido"],
                        "description": "A nova etapa do funil: 'qualificacao' (se souber o nome e procedimento de interesse do paciente) ou 'perdido' (se o cliente desistir ou recusar)."
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
    # Retorna apenas nome, descrição e duração (sem valores)
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "duration_minutes": p.duration_minutes
        } for p in procedures
    ]

def get_doctors_db():
    try:
        doctors = Doctor.query.all()
        return [
            {
                "id": d.id,
                "name": d.name,
                "specialty": d.specialty
            } for d in doctors
        ]
    except Exception as e:
        logging.error(f"Erro ao buscar médicos: {e}")
        return []

def request_appointment_db(patient, patient_name, procedure_name, doctor_name=None, preferred_time=None):
    try:
        if patient_name:
            patient.name = patient_name
        patient.kanban_stage = 'agendamento_pendente'
        patient.ai_enabled = False
        db.session.commit()
        return {
            "success": True,
            "message": "O agendamento pendente foi registrado com sucesso e a IA da Unic Clinic foi pausada. Um atendente humano assumirá a conversa para escolher o melhor horário."
        }
    except Exception as e:
        logging.error(f"Erro ao registrar transbordo: {e}")
        return {"error": str(e)}


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
            if settings.beta_mode_enabled:
                if is_allowed:
                    patient.ai_enabled = True
                else:
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
                    elif function_name == "get_doctors":
                        tool_result = get_doctors_db()
                    elif function_name == "request_appointment":
                        tool_result = request_appointment_db(
                            patient=patient,
                            patient_name=function_args.get("patient_name"),
                            procedure_name=function_args.get("procedure_name"),
                            doctor_name=function_args.get("doctor_name"),
                            preferred_time=function_args.get("preferred_time")
                        )
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
