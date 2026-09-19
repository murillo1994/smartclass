import logging
from flask import Flask, jsonify
from src.config import Config
from src.routes.telemetry_routes import telemetry_bp
from src.routes.auth_routes import auth_bp
from src.database import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    """Application Factory do Flask para o SmartClass."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Registrar blueprints
    app.register_blueprint(telemetry_bp)
    app.register_blueprint(auth_bp)

    # Configuração de CORS para permitir requisições assíncronas do frontend estático
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

    # Handlers globais para respostas semânticas padronizadas
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "status": "error",
            "message": "Requisição inválida.",
            "code": 400
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "status": "error",
            "message": "Recurso não encontrado.",
            "code": 404
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "status": "error",
            "message": "Método HTTP não permitido para este endpoint.",
            "code": 405
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "status": "error",
            "message": "Erro interno do servidor.",
            "code": 500
        }), 500

    import os
    from flask import send_from_directory

    possible_frontend_dirs = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend")),
        "/app/frontend",
        "/root/smartclass/frontend"
    ]
    frontend_dir = next((d for d in possible_frontend_dirs if os.path.isdir(d)), possible_frontend_dirs[0])

    # Rota raiz básica
    @app.route("/", methods=["GET"])
    def root():
        if os.path.exists(os.path.join(frontend_dir, "dashboard.html")):
            return send_from_directory(frontend_dir, "dashboard.html")
        return jsonify({
            "message": "SmartClass IoT Telemetry Ingestion Service",
            "version": "1.0.0",
            "status": "online"
        }), 200

    @app.route("/dashboard", methods=["GET"])
    @app.route("/dashboard.html", methods=["GET"])
    def dashboard():
        return send_from_directory(frontend_dir, "dashboard.html")

    @app.route("/login", methods=["GET"])
    @app.route("/login.html", methods=["GET"])
    def login_page():
        return send_from_directory(frontend_dir, "login.html")

    @app.route("/js/<path:filename>", methods=["GET"])
    def serve_js(filename):
        return send_from_directory(os.path.join(frontend_dir, "js"), filename)

    # Tenta inicializar as tabelas do banco de dados na inicialização
    try:
        init_db()
    except Exception as e:
        logger.warning(f"Inicialização automática do banco postergada: {e}")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=Config.PORT, debug=Config.DEBUG)
