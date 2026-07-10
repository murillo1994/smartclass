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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
