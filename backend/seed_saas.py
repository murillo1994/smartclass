import sys
import os
from datetime import datetime, timedelta

from src.app import create_app
from src.database import (
    db, Tenant, User, WhatsAppInstance, Funnel, FunnelStage, 
    Contact, Conversation, Message, InternalNote, Tag, QuickReply
)

def seed_saas():
    app = create_app()
    with app.app_context():
        print("Recreando tabelas com o novo schema Multi-Tenant...")
        db.drop_all()
        db.create_all()

        # 1. SuperAdmin
        super_admin = User.query.filter_by(email='super@crm.com').first()
        if not super_admin:
            super_admin = User(
                name='Suporte Master CRM',
                email='super@crm.com',
                role='superadmin',
                active=True
            )
            super_admin.set_password('admin123')
            db.session.add(super_admin)
            print("SuperAdmin criado: super@crm.com / admin123")

        # 2. Empresa Alpha (Pro)
        tenant_alpha = Tenant.query.filter_by(slug='clinica-alpha').first()
        if not tenant_alpha:
            tenant_alpha = Tenant(
                name='Clínica Alpha Estética',
                slug='clinica-alpha',
                document='12.345.678/0001-90',
                status='active',
                plan_name='pro',
                max_users=5,
                max_instances=2
            )
            db.session.add(tenant_alpha)
            db.session.flush()

            # Admin Alpha
            admin_alpha = User(
                tenant_id=tenant_alpha.id,
                name='Dra. Mariana Alpha',
                email='admin@clinicaalpha.com',
                role='admin',
                active=True
            )
            admin_alpha.set_password('admin123')
            db.session.add(admin_alpha)

            # Atendente Alpha
            user_alpha = User(
                tenant_id=tenant_alpha.id,
                name='Lucas Atendente',
                email='atendente1@clinicaalpha.com',
                role='attendant',
                active=True
            )
            user_alpha.set_password('admin123')
            db.session.add(user_alpha)
            db.session.flush()

            # WhatsApp Instâncias da Alpha (2 números)
            inst_vendas = WhatsAppInstance(
                tenant_id=tenant_alpha.id,
                name='Vendas & Agendamento',
                instance_name=f'tenant_{tenant_alpha.slug}_vendas',
                phone_number='5511999887766',
                status='connected'
            )
            inst_suporte = WhatsAppInstance(
                tenant_id=tenant_alpha.id,
                name='SAC & Dúvidas',
                instance_name=f'tenant_{tenant_alpha.slug}_sac',
                phone_number='5511988776655',
                status='connected'
            )
            db.session.add_all([inst_vendas, inst_suporte])
            db.session.flush()

            # Funil & Etapas
            funnel_alpha = Funnel(
                tenant_id=tenant_alpha.id,
                name='Funil de Vendas Geral',
                is_default=True
            )
            db.session.add(funnel_alpha)
            db.session.flush()

            stages = [
                FunnelStage(tenant_id=tenant_alpha.id, funnel_id=funnel_alpha.id, name='Lead Novo', color='#3b82f6', order_position=0),
                FunnelStage(tenant_id=tenant_alpha.id, funnel_id=funnel_alpha.id, name='Qualificação', color='#eab308', order_position=1),
                FunnelStage(tenant_id=tenant_alpha.id, funnel_id=funnel_alpha.id, name='Proposta Enviada', color='#8b5cf6', order_position=2),
                FunnelStage(tenant_id=tenant_alpha.id, funnel_id=funnel_alpha.id, name='Fechado / Ganho', color='#10b981', order_position=3)
            ]
            db.session.add_all(stages)
            db.session.flush()

            # Tags
            tag_vip = Tag(tenant_id=tenant_alpha.id, name='VIP', color='#ef4444')
            tag_urgente = Tag(tenant_id=tenant_alpha.id, name='Urgente', color='#f97316')
            db.session.add_all([tag_vip, tag_urgente])

            # Respostas Rápidas
            quick_pix = QuickReply(
                tenant_id=tenant_alpha.id,
                shortcut='/pix',
                title='Chave PIX da Clínica',
                message='Nossa chave PIX CNPJ é: 12.345.678/0001-90 (Banco Inter). Assim que realizar o pagamento, por favor nos envie o comprovante por aqui!'
            )
            quick_ola = QuickReply(
                tenant_id=tenant_alpha.id,
                shortcut='/ola',
                title='Saudação Padrão',
                message='Olá! Seja muito bem-vindo(a) à Clínica Alpha. Como podemos transformar seu bem-estar hoje?'
            )
            db.session.add_all([quick_pix, quick_ola])

            # Contatos & Conversas
            c1 = Contact(
                tenant_id=tenant_alpha.id,
                remote_jid='5511977665544@s.whatsapp.net',
                phone='5511977665544',
                name='Fernanda Souza',
                current_stage_id=stages[1].id,
                assigned_user_id=user_alpha.id
            )
            c1.tags.append(tag_vip)
            db.session.add(c1)
            db.session.flush()

            conv1 = Conversation(
                tenant_id=tenant_alpha.id,
                instance_id=inst_vendas.id,
                contact_id=c1.id,
                assigned_user_id=user_alpha.id,
                status='open',
                unread_count=0
            )
            db.session.add(conv1)
            db.session.flush()

            m1 = Message(
                tenant_id=tenant_alpha.id,
                conversation_id=conv1.id,
                sender_type='contact',
                content='Olá! Gostaria de saber mais sobre o protocolo de rejuvenescimento.',
                created_at=datetime.utcnow() - timedelta(minutes=15)
            )
            m2 = Message(
                tenant_id=tenant_alpha.id,
                conversation_id=conv1.id,
                sender_type='attendant',
                user_id=user_alpha.id,
                content='Olá Fernanda! Claro, temos o protocolo completo com avaliação personalizada.',
                created_at=datetime.utcnow() - timedelta(minutes=10)
            )
            note1 = InternalNote(
                tenant_id=tenant_alpha.id,
                conversation_id=conv1.id,
                user_id=user_alpha.id,
                content='Paciente tem interesse em preenchimento e botox para o casamento em novembro.'
            )
            db.session.add_all([m1, m2, note1])
            print("Empresa Alpha criada com sucesso!")

        # 3. Empresa Beta (Starter)
        tenant_beta = Tenant.query.filter_by(slug='estetica-beta').first()
        if not tenant_beta:
            tenant_beta = Tenant(
                name='Espaço Estética Beta',
                slug='estetica-beta',
                document='98.765.432/0001-10',
                status='active',
                plan_name='starter',
                max_users=2,
                max_instances=1
            )
            db.session.add(tenant_beta)
            db.session.flush()

            admin_beta = User(
                tenant_id=tenant_beta.id,
                name='Dr. Rodrigo Beta',
                email='admin@esteticabeta.com',
                role='admin',
                active=True
            )
            admin_beta.set_password('admin123')
            db.session.add(admin_beta)

            inst_beta = WhatsAppInstance(
                tenant_id=tenant_beta.id,
                name='Recepção Geral',
                instance_name=f'tenant_{tenant_beta.slug}_geral',
                phone_number='5521999112233',
                status='connected'
            )
            db.session.add(inst_beta)
            db.session.flush()

            funnel_beta = Funnel(tenant_id=tenant_beta.id, name='Funil Principal', is_default=True)
            db.session.add(funnel_beta)
            db.session.flush()

            stg_beta = [
                FunnelStage(tenant_id=tenant_beta.id, funnel_id=funnel_beta.id, name='Novos Contatos', color='#3b82f6', order_position=0),
                FunnelStage(tenant_id=tenant_beta.id, funnel_id=funnel_beta.id, name='Em Atendimento', color='#eab308', order_position=1),
                FunnelStage(tenant_id=tenant_beta.id, funnel_id=funnel_beta.id, name='Concluído', color='#10b981', order_position=2)
            ]
            db.session.add_all(stg_beta)

            print("Empresa Beta criada com sucesso!")

        db.session.commit()
        print("Semeação do SaaS finalizada com sucesso!")

if __name__ == '__main__':
    seed_saas()
