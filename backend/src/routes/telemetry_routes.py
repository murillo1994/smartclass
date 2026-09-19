import logging
from flask import Blueprint, request, jsonify
from src.services.telemetry_service import TelemetryService, ValidationError

logger = logging.getLogger(__name__)
telemetry_bp = Blueprint("telemetry", __name__, url_prefix="/api/v1")

service = TelemetryService()

@telemetry_bp.route("/medicoes", methods=["POST"])
def post_medicao():
    """Endpoint para recepção e ingestão de telemetria enviada pelo hardware IoT."""
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Cabeçalho Content-Type deve ser 'application/json'.",
            "code": 400
        }), 400

    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({
            "status": "error",
            "message": "Payload JSON ausente ou malformado.",
            "code": 400
        }), 400

    try:
        leitura = service.register_measurement(payload)
        return jsonify({
            "status": "success",
            "message": "Medição registrada com sucesso.",
            "data": leitura.to_dict()
        }), 201

    except ValidationError as ve:
        logger.warning(f"Rejeição de payload de telemetria: {ve}")
        return jsonify({
            "status": "error",
            "message": str(ve),
            "code": 400
        }), 400

    except Exception as e:
        logger.error(f"Erro inesperado ao persistir telemetria: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": "Falha na camada de persistência dos dados.",
            "code": 500
        }), 500

@telemetry_bp.route("/medicoes/recent", methods=["GET"])
def get_recent_medicoes():
    """Endpoint auxiliar para listar as medições mais recentes."""
    try:
        limit = request.args.get("limit", default=50, type=int)
        leituras = service.repository.list_recent(limit=limit)
        return jsonify({
            "status": "success",
            "data": [l.to_dict() for l in leituras]
        }), 200
    except Exception as e:
        logger.error(f"Erro ao recuperar histórico recente: {e}")
        return jsonify({
            "status": "error",
            "message": "Falha ao consultar leituras no banco de dados.",
            "code": 500
        }), 500

@telemetry_bp.route("/health", methods=["GET"])
def health_check():
    """Endpoint de verificação de integridade da API."""
    return jsonify({
        "status": "healthy",
        "service": "SmartClass IoT Telemetry Ingestion API"
    }), 200
