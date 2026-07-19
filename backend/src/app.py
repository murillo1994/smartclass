from flask import Flask, jsonify
from flask_cors import CORS
from src.config import Config
from src.database import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for frontend requests
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize extensions
    db.init_app(app)

    # Register blueprints (routes)
    from src.routes.webhook import webhook_bp
    from src.routes.api import api_bp

    app.register_blueprint(webhook_bp, url_prefix='/webhook')
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def health():
        return jsonify({"status": "healthy", "service": "unic_backend"}), 200

    # Automatically create database tables within application context
    with app.app_context():
        db.create_all()
        # Check and add missing columns to patients table
        try:
            from sqlalchemy import text
            result = db.session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='patients'"))
            existing_cols = [row[0] for row in result.fetchall()]
            
            if 'is_imported' not in existing_cols:
                db.session.execute(text("ALTER TABLE patients ADD COLUMN is_imported BOOLEAN DEFAULT FALSE NOT NULL"))
                db.session.commit()
                logging.info("Added missing column 'is_imported' to 'patients' table.")
                
            if 'ignored' not in existing_cols:
                db.session.execute(text("ALTER TABLE patients ADD COLUMN ignored BOOLEAN DEFAULT FALSE NOT NULL"))
                db.session.commit()
                logging.info("Added missing column 'ignored' to 'patients' table.")
        except Exception as e:
            logging.error(f"Error checking/migrating patients table columns: {e}")

        # Check and add missing columns to system_settings table
        try:
            from sqlalchemy import text
            result = db.session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='system_settings'"))
            existing_settings_cols = [row[0] for row in result.fetchall()]
            
            new_settings_cols = {
                'clinic_name': "VARCHAR(255) DEFAULT 'Unic Clinic'",
                'clinic_address': "TEXT DEFAULT ''",
                'clinic_phones': "VARCHAR(255) DEFAULT ''",
                'clinic_addresses': "TEXT DEFAULT '[]'",
                'clinic_phones_list': "TEXT DEFAULT '[]'",
                'clinic_instagram': "VARCHAR(255) DEFAULT ''",
                'clinic_responsible': "VARCHAR(255) DEFAULT ''",
                'clinic_working_hours': "VARCHAR(255) DEFAULT 'Segunda a Sexta, das 09:00 às 18:00'",
                'clinic_custom_notes': "TEXT DEFAULT ''",
                'clinic_custom_rules': "TEXT DEFAULT '[]'"
            }
            
            for col_name, col_def in new_settings_cols.items():
                if col_name not in existing_settings_cols:
                    db.session.execute(text(f"ALTER TABLE system_settings ADD COLUMN {col_name} {col_def}"))
                    db.session.commit()
                    logging.info(f"Added missing column '{col_name}' to 'system_settings' table.")
        except Exception as e:
            logging.error(f"Error checking/migrating system_settings table columns: {e}")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
