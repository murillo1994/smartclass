from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# Initialize Flask SQLAlchemy extension instance
db = SQLAlchemy()

# Define Enum values for database integrity
FASE_FUNIL_ENUM = ('lead_novo', 'qualificacao', 'agendamento_pendente', 'agendado', 'perdido', 'concluido')
ORIGEM_MSG_ENUM = ('paciente', 'bot', 'recepcao')
STATUS_AGENDA_ENUM = ('pendente', 'confirmado', 'cancelado', 'compareceu', 'no_show')
TIPO_MIDIA_ENUM = ('texto', 'audio', 'imagem', 'video', 'documento')

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    kanban_stage = db.Column(
        db.Enum(*FASE_FUNIL_ENUM, name='enum_fase_funil'), 
        nullable=False, 
        default='lead_novo'
    )
    ai_enabled = db.Column(db.Boolean, nullable=False, default=True)
    is_imported = db.Column(db.Boolean, nullable=False, default=False)
    ignored = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    
    appointments = db.relationship('Appointment', backref='patient', cascade='all, delete-orphan', lazy=True)
    messages = db.relationship('Message', backref='patient', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'kanban_stage': self.kanban_stage,
            'ai_enabled': self.ai_enabled,
            'is_imported': self.is_imported,
            'ignored': self.ignored,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    specialty = db.Column(db.String(255), nullable=False)
    
    availabilities = db.relationship('DoctorAvailability', backref='doctor', cascade='all, delete-orphan', lazy=True)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty
        }

class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availabilities'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False) # 0 = Segunda, 4 = Sexta
    start_time = db.Column(db.String(5), nullable=False)
    end_time = db.Column(db.String(5), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'doctor_id': self.doctor_id,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

class Procedure(db.Model):
    __tablename__ = 'procedures'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration_minutes = db.Column(db.Integer, nullable=False, default=30)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'duration_minutes': self.duration_minutes,
            'price': float(self.price)
        }

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    procedure_id = db.Column(db.Integer, db.ForeignKey('procedures.id', ondelete='RESTRICT'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(
        db.Enum(*STATUS_AGENDA_ENUM, name='enum_status_agenda'), 
        nullable=False, 
        default='pendente'
    )
    created_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'procedure_id': self.procedure_id,
            'doctor_id': self.doctor_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False)
    sender = db.Column(
        db.Enum(*ORIGEM_MSG_ENUM, name='enum_origem_msg'), 
        nullable=False
    )
    content = db.Column(db.Text, nullable=False)
    media_type = db.Column(
        db.Enum(*TIPO_MIDIA_ENUM, name='enum_tipo_midia'), 
        nullable=False, 
        default='texto'
    )
    created_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'sender': self.sender,
            'content': self.content,
            'media_type': self.media_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SystemSettings(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    beta_mode_enabled = db.Column(db.Boolean, nullable=False, default=True)
    beta_allowed_numbers = db.Column(db.Text, nullable=False, default='')
    auto_activate_ai_for_new_leads = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'beta_mode_enabled': self.beta_mode_enabled,
            'beta_allowed_numbers': self.beta_allowed_numbers,
            'auto_activate_ai_for_new_leads': self.auto_activate_ai_for_new_leads
        }
