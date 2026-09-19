import pytest

def test_successful_temperature_ingestion(client):
    """Testa o fluxo principal (Golden Path) de ingestão de temperatura (US1)."""
    payload = {
        "sala_id": "Sala 101",
        "temperatura": 24.5
    }
    response = client.post(
        "/api/v1/medicoes",
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["id"] == 1
    assert data["data"]["sala_id"] == "Sala 101"
    assert data["data"]["temperatura"] == 24.5
    assert data["data"]["umidade"] is None
    assert "data_registro" in data["data"]

def test_recent_medicoes_endpoint(client):
    """Testa a listagem de telemetrias após inserção."""
    client.post("/api/v1/medicoes", json={"sala_id": "Sala 102", "temperatura": 22.0})
    response = client.get("/api/v1/medicoes/recent")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert len(data["data"]) >= 1
