import os
import sys
from datetime import datetime, timedelta

from src.app import create_app
from src.database import db, Patient, Message, Procedure, Appointment, Doctor, DoctorAvailability

def seed_fake_leads():
    app = create_app()
    with app.app_context():
        print("Recreando tabelas do banco de dados (Drop & Create)...")
        db.drop_all()
        db.create_all()
        print("Tabelas recreadas com sucesso!")

        # 1. Semear Procedimentos
        print("Cadastrando procedimentos estéticos premium da Unic Clinic...")
        procedures = [
            Procedure(
                name="Toxina Botulínica (Botox)",
                description="Suavização de linhas de expressão e rugas dinâmicas da testa, glabela e olhos (pés de galinha).",
                duration_minutes=30,
                price=1200.00
            ),
            Procedure(
                name="Preenchimento Labial",
                description="Escultura labial com ácido hialurônico para volumização, definição de contorno e hidratação.",
                duration_minutes=45,
                price=1500.00
            ),
            Procedure(
                name="Harmonização Facial",
                description="Conjunto de procedimentos estéticos combinados para melhorar a simetria do rosto e contorno mandibular.",
                duration_minutes=60,
                price=3500.00
            ),
            Procedure(
                name="Bioestimulador de Colágeno",
                description="Aplicação profunda de Sculptra ou Radiesse para reestruturação da pele e tratamento da flacidez.",
                duration_minutes=45,
                price=2200.00
            ),
            Procedure(
                name="Peeling Químico Cristal",
                description="Renovação celular e clareamento de manchas faciais através de ácidos específicos de alta performance.",
                duration_minutes=30,
                price=450.00
            )
        ]
        db.session.bulk_save_objects(procedures)
        db.session.commit()
        print("5 procedimentos adicionados.")

        # 2. Semear Médicos & Especialistas
        print("Cadastrando corpo clínico boutique...")
        doctors = [
            Doctor(name="Dra. Ana Paula", specialty="Dermatologista Esteta"),
            Doctor(name="Dr. Lucas Ramos", specialty="Terapeuta Capilar Tricologista"),
            Doctor(name="Dra. Mariana Rocha", specialty="Fisioterapeuta Dermato-Funcional")
        ]
        db.session.add_all(doctors)
        db.session.commit()
        print("3 especialistas adicionados.")

        # Cadastrar disponibilidade padrão para os médicos (Segunda a Sexta das 09:00 às 18:00)
        for doc in doctors:
            for day in range(5): # 0 = Segunda, 4 = Sexta
                avail = DoctorAvailability(
                    doctor_id=doc.id,
                    day_of_week=day,
                    start_time="09:00",
                    end_time="18:00"
                )
                db.session.add(avail)
        db.session.commit()
        print("Disponibilidades semanais configuradas para os especialistas.")

        # 3. Semear Leads
        print("Cadastrando 10 leads de teste com diferentes fases e diálogos...")
        fake_data = [
            {
                "name": "Mariana Silva",
                "phone": "5512990000001",
                "kanban_stage": "lead_novo",
                "ai_enabled": True,
                "dialog": [
                    {"sender": "paciente", "content": "Olá, vi o site de vocês e gostaria de saber o valor do Peeling Cristal."},
                    {"sender": "bot", "content": "Olá, Mariana! Tudo bem? O nosso Peeling Cristal está a partir de R$ 450,00 e a sessão dura cerca de 30 minutos. Gostaria de agendar uma avaliação?"}
                ]
            },
            {
                "name": "Beatriz Souza",
                "phone": "5512990000002",
                "kanban_stage": "qualificacao",
                "ai_enabled": True,
                "dialog": [
                    {"sender": "paciente", "content": "Queria entender qual a diferença do Botox para o Preenchimento Labial."},
                    {"sender": "bot", "content": "Excelente dúvida, Beatriz! O Botox é usado para relaxar os músculos e suavizar rugas e marcas de expressão (como na testa e ao redor dos olhos). Já o Preenchimento Labial utiliza ácido hialurônico para dar volume, definição e contorno direto nos lábios. Cada um tem um propósito diferente!"},
                    {"sender": "paciente", "content": "Ah sim! Eu tenho interesse em fazer nos lábios. Vocês usam anestesia?"}
                ]
            },
            {
                "name": "Carla Dias",
                "phone": "5512990000003",
                "kanban_stage": "agendamento_pendente",
                "ai_enabled": True,
                "dialog": [
                    {"sender": "paciente", "content": "Quero fazer uma Harmonização Facial. Vocês têm horários disponíveis nesta quinta-feira?"},
                    {"sender": "bot", "content": "Com certeza, Carla! Para esta quinta-feira, temos horários disponíveis às 10:30, 14:00 e 16:30. Qual desses horários fica melhor para você reservar?"}
                ]
            },
            {
                "name": "Débora Santos",
                "phone": "5512990000004",
                "kanban_stage": "agendado",
                "ai_enabled": True,
                "dialog": [
                    {"sender": "paciente", "content": "Queria agendar uma aplicação de Toxina Botulínica."},
                    {"sender": "bot", "content": "Perfeito, Débora! Consegui agendar para você na sexta-feira, dia 17 de julho, às 14:00. O agendamento está confirmado!"},
                    {"sender": "paciente", "content": "Ótimo! Estarei aí no horário marcado. Obrigado."}
                ],
                "appointment": {
                    "procedure_name": "Toxina Botulínica (Botox)",
                    "doctor_name": "Dra. Ana Paula",
                    "days_offset": 7,
                    "hour": 14,
                    "minute": 0
                }
            },
            {
                "name": "Elisa Mendes",
                "phone": "5512990000005",
                "kanban_stage": "perdido",
                "ai_enabled": True,
                "dialog": [
                    {"sender": "paciente", "content": "Olá, qual o valor da Harmonização Facial?"},
                    {"sender": "bot", "content": "Olá, Elisa! A nossa Harmonização Facial completa está a partir de R$ 3.500,00, variando conforme a avaliação médica das suas proporções. Podemos agendar uma consulta para você?"},
                    {"sender": "paciente", "content": "Nossa, achei um pouco caro no momento, mas agradeço a atenção. Quem sabe na próxima!"}
                ]
            },
            {
                "name": "Gabriela Costa",
                "phone": "5512990000006",
                "kanban_stage": "concluido",
                "ai_enabled": False, # Handoff realizado/concluido
                "dialog": [
                    {"sender": "paciente", "content": "Já fiz minha consulta e amei o resultado! Queria apenas tirar uma dúvida sobre a lavagem do rosto pós-peeling."},
                    {"sender": "recepcao", "content": "Olá, Gabriela! Ficamos extremamente felizes que tenha gostado! Evite lavar o rosto com água quente nas primeiras 24h e use bastante o protetor solar indicado pela Dra. Qualquer dúvida estamos à disposição!"}
                ]
            },
            {
                "name": "Juliana Rocha",
                "phone": "5512990000007",
                "kanban_stage": "lead_novo",
                "ai_enabled": True,
                "dialog": [
                    {"sender": "paciente", "content": "Oi, vocês trabalham com tratamento de queda de cabelo?"}
                ]
            },
            {
                "name": "Larissa Faria",
                "phone": "5512990000008",
                "kanban_stage": "qualificacao",
                "ai_enabled": True,
                "dialog": [
                    {"sender": "paciente", "content": "Olá! Gostaria de saber se o Bioestimulador de Colágeno ajuda a tratar a flacidez no pescoço."},
                    {"sender": "bot", "content": "Olá, Larissa! Ajuda sim, e o resultado é excelente! O bioestimulador (como o Sculptra) estimula a produção natural do seu colágeno, devolvendo firmeza e contorno para a região do pescoço e colo. Costuma durar até 25 meses. Quer agendar uma avaliação?"},
                    {"sender": "paciente", "content": "Sim, eu quero. Mas antes, dói muito para aplicar?"}
                ]
            },
            {
                "name": "Fernanda Lima",
                "phone": "5512990000009",
                "kanban_stage": "agendamento_pendente",
                "ai_enabled": True,
                "dialog": [
                    {"sender": "paciente", "content": "Quais horários vocês têm livres amanhã de tarde?"},
                    {"sender": "bot", "content": "Oi, Fernanda! Amanhã na parte da tarde temos horários livres às 14:30 e às 16:00. Algum deles é bom para você?"}
                ]
            },
            {
                "name": "Amanda Oliveira",
                "phone": "5512990000010",
                "kanban_stage": "agendado",
                "ai_enabled": True,
                "dialog": [
                    {"sender": "paciente", "content": "Gostaria de marcar uma avaliação."},
                    {"sender": "bot", "content": "Perfeito, Amanda! Agendei seu atendimento para amanhã às 10:00. Nos vemos lá!"}
                ],
                "appointment": {
                    "procedure_name": "Toxina Botulínica (Botox)",
                    "doctor_name": "Dra. Ana Paula",
                    "days_offset": 1,
                    "hour": 10,
                    "minute": 0
                }
            }
        ]

        # Inserir leads e diálogos
        for item in fake_data:
            patient = Patient(
                name=item["name"],
                phone=item["phone"],
                kanban_stage=item["kanban_stage"],
                ai_enabled=item["ai_enabled"]
            )
            db.session.add(patient)
            db.session.commit()

            # Salvar diálogos
            for msg in item["dialog"]:
                message = Message(
                    patient_id=patient.id,
                    sender=msg["sender"],
                    content=msg["content"]
                )
                db.session.add(message)
            db.session.commit()

            # Criar agendamento se especificado
            if "appointment" in item:
                proc_name = item["appointment"]["procedure_name"]
                doc_name = item["appointment"]["doctor_name"]
                
                procedure = Procedure.query.filter(Procedure.name.like(f"%{proc_name}%")).first()
                doctor = Doctor.query.filter(Doctor.name.like(f"%{doc_name}%")).first()
                
                if procedure and doctor:
                    start_date = datetime.now() + timedelta(days=item["appointment"]["days_offset"])
                    start_time = datetime.combine(
                        start_date.date(),
                        datetime.strptime(f"{item['appointment']['hour']}:{item['appointment']['minute']}", "%H:%M").time()
                    )
                    end_time = start_time + timedelta(minutes=procedure.duration_minutes)

                    appt = Appointment(
                        patient_id=patient.id,
                        procedure_id=procedure.id,
                        doctor_id=doctor.id,
                        start_time=start_time,
                        end_time=end_time,
                        status='confirmado'
                    )
                    db.session.add(appt)
                    db.session.commit()

        print("Semeação concluída com sucesso! Banco totalmente recreado e populado.")

if __name__ == '__main__':
    seed_fake_leads()
