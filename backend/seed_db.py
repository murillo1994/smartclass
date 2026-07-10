import os
import sys

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from app import create_app
from database import db, Procedure

def seed_procedures():
    app = create_app()
    with app.app_context():
        # Check if procedures already exist
        if Procedure.query.first():
            print("Procedimentos já cadastrados no banco de dados. Pulando semeação.")
            return

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
        print("Semeação concluída com sucesso! 5 procedimentos adicionados.")

if __name__ == '__main__':
    seed_procedures()
