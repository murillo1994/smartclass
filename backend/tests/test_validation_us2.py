import pytest

def test_missing_temperatura_field(client):
    """Testa rejeição de payload sem a chave 'temperatura' (US2)."""
    response = client.post(
        "/api/v1/medicoes",
        json={"sala_id": "Sala 101"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "temperatura" in data["message"]

def test_missing_sala_id_field(client):
    """Testa rejeição de payload sem a chave 'sala_id' (US2)."""
    response = client.post(
        "/api/v1/medicoes",
        json={"temperatura": 25.0}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
    assert "sala_id" in data["message"]

def test_empty_sala_id(client):
    """Testa rejeição de 'sala_id' vazio."""
    response = client.post(
        "/api/v1/medicoes",
        json={"sala_id": "   ", "temperatura": 25.0}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"

def test_sala_id_too_long(client):
    """Testa rejeição de 'sala_id' com mais de 50 caracteres."""
    response = client.post(
        "/api/v1/medicoes",
        json={"sala_id": "A" * 51, "temperatura": 25.0}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"

def test_non_numeric_temperatura(client):
    """Testa rejeição de temperatura não numérica."""
    response = client.post(
        "/api/v1/medicoes",
        json={"sala_id": "Sala 101", "temperatura": "vinte_graus"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"

def test_extreme_temperatura_out_of_range(client):
    """Testa rejeição de temperatura fora da faixa física."""
    response = client.post(
        "/api/v1/medicoes",
        json={"sala_id": "Sala 101", "temperatura": 150.0}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"

def test_invalid_content_type(client):
    """Testa rejeição quando Content-Type não é JSON."""
    response = client.post(
        "/api/v1/medicoes",
        data="plain text reading",
        headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"
