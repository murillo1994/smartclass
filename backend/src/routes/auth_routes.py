import os
import secrets
import logging
from flask import Blueprint, request, jsonify

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    """Endpoint RESTful para autenticação de operadores do SmartClass."""
    valid_username = os.getenv("SMARTCLASS_USER", "admin")
    valid_password = os.getenv("SMARTCLASS_PASS", "admin123")

    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "O corpo da requisição deve ser no formato JSON.",
            "code": 400
        }), 400

    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()

    if not username or not password:
        return jsonify({
            "status": "error",
            "message": "Informe o usuário e a senha para acessar.",
            "code": 400
        }), 400

    if username == valid_username and password == valid_password:
        token = f"sc_token_{secrets.token_hex(16)}"
        logger.info(f"Login bem-sucedido para operador: '{username}'")
        return jsonify({
            "status": "success",
            "message": "Autenticação realizada com sucesso.",
            "token": token,
            "user": {
                "username": username,
                "name": "Operador Univesp",
                "role": "Administrador",
                "institution": "Universidade Virtual do Estado de São Paulo"
            }
        }), 200

    logger.warning(f"Tentativa de login inválida para o usuário: '{username}'")
    return jsonify({
        "status": "error",
        "message": "Usuário ou senha incorretos. Verifique suas credenciais.",
        "code": 401
    }), 401
