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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
