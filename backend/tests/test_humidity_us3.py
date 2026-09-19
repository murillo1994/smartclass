import pytest
from unittest.mock import MagicMock

def test_successful_combined_humidity_ingestion(client):
    """Testa a ingestão bem-sucedida de telemetria com umidade opcional (US3)."""
    payload = {
        "sala_id": "Lab 02",
        "temperatura": 22.0,
        "umidade": 65.5
    }
    response = client.post(
        "/api/v1/medicoes",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["temperatura"] == 22.0
    assert data["data"]["umidade"] == 65.5

def test_invalid_humidity_above_100(client):
    """Testa rejeição de umidade acima de 100%."""
    payload = {
        "sala_id": "Lab 02",
        "temperatura": 22.0,
        "umidade": 105.0
    }
    response = client.post("/api/v1/medicoes", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "umidade" in data["message"]

def test_invalid_humidity_negative(client):
    """Testa rejeição de umidade negativa."""
    payload = {
        "sala_id": "Lab 02",
        "temperatura": 22.0,
        "umidade": -2.0
    }
    response = client.post("/api/v1/medicoes", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"

def test_database_error_handling(client, monkeypatch):
    """Testa retorno HTTP 500 semântico quando o banco de dados falha."""
    from src.routes import telemetry_routes
    
    mock_failing_repo = MagicMock()
    mock_failing_repo.insert.side_effect = RuntimeError("Conexão com banco perdida")
    
    monkeypatch.setattr(telemetry_routes.service, "repository", mock_failing_repo)

    response = client.post(
        "/api/v1/medicoes",
        json={"sala_id": "Sala 101", "temperatura": 23.0}
    )
    assert response.status_code == 500
    data = response.get_json()
    assert data["status"] == "error"
    assert data["code"] == 500
