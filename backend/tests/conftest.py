import pytest
from datetime import datetime, timezone
from src.app import create_app
from src.models.telemetry import LeituraSensor
from src.repositories.telemetry_repo import TelemetryRepository

class MockTelemetryRepository(TelemetryRepository):
    """Repositório em memória para execução de testes unitários e de contrato."""

    def __init__(self):
        self.records = []
        self._next_id = 1

    def insert(self, leitura: LeituraSensor) -> LeituraSensor:
        record = LeituraSensor(
            id=self._next_id,
            sala_id=leitura.sala_id,
            temperatura=leitura.temperatura,
            umidade=leitura.umidade,
            data_registro=datetime.now(timezone.utc)
        )
        self.records.append(record)
        self._next_id += 1
        return record

    def find_by_id(self, reading_id: int):
        for r in self.records:
            if r.id == reading_id:
                return r
        return None

    def list_recent(self, limit: int = 50):
        return sorted(self.records, key=lambda r: r.data_registro, reverse=True)[:limit]

@pytest.fixture
def mock_repo():
    return MockTelemetryRepository()

@pytest.fixture
def app(mock_repo):
    app = create_app()
    app.config["TESTING"] = True
    
    # Injeta mock no serviço da rota
    from src.routes import telemetry_routes
    telemetry_routes.service.repository = mock_repo
    
    return app

@pytest.fixture
def client(app):
    return app.test_client()
