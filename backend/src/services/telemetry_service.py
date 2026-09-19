import logging
from typing import Tuple, Optional, Dict, Any
from src.models.telemetry import LeituraSensor
from src.repositories.telemetry_repo import TelemetryRepository

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Exceção customizada para erros de validação de payload."""
    pass

class TelemetryService:
    """Serviço de validação e orquestração de telemetria."""

    def __init__(self, repository: Optional[TelemetryRepository] = None):
        self.repository = repository or TelemetryRepository()

    def validate_payload(self, data: Any) -> Dict[str, Any]:
        """Valida estruturalmente o payload de telemetria recebido do IoT."""
        if not isinstance(data, dict):
            raise ValidationError("Payload ausente ou não formatado como objeto JSON válido.")

        # Validação do campo obrigatório: sala_id
        if "sala_id" not in data:
            raise ValidationError("Campo obrigatório ausente: 'sala_id'")
        
        sala_id = data["sala_id"]
        if not isinstance(sala_id, str) or not sala_id.strip():
            raise ValidationError("O campo 'sala_id' deve ser uma string não vazia.")
        
        if len(sala_id) > 50:
            raise ValidationError("O campo 'sala_id' deve ter no máximo 50 caracteres.")

        # Validação do campo obrigatório: temperatura
        if "temperatura" not in data:
            raise ValidationError("Campo obrigatório ausente: 'temperatura'")

        temp_val = data["temperatura"]
        if isinstance(temp_val, bool) or not isinstance(temp_val, (int, float)):
            raise ValidationError("O campo 'temperatura' deve ser um valor numérico.")

        temperatura = float(temp_val)
        if temperatura < -40.0 or temperatura > 85.0:
            raise ValidationError("O campo 'temperatura' está fora da faixa física suportada (-40°C a 85°C).")

        # Validação do campo opcional: umidade
        umidade = None
        if "umidade" in data and data["umidade"] is not None:
            umid_val = data["umidade"]
            if isinstance(umid_val, bool) or not isinstance(umid_val, (int, float)):
                raise ValidationError("O campo 'umidade' deve ser um valor numérico.")
            
            umidade = float(umid_val)
            if umidade < 0.0 or umidade > 100.0:
                raise ValidationError("O campo 'umidade' deve estar compreendido entre 0% e 100%.")

        return {
            "sala_id": sala_id.strip(),
            "temperatura": round(temperatura, 2),
            "umidade": round(umidade, 2) if umidade is not None else None
        }

    def register_measurement(self, payload: Any) -> LeituraSensor:
        """Valida os dados e persiste uma nova medição através do repositório."""
        validated_data = self.validate_payload(payload)
        leitura = LeituraSensor(
            sala_id=validated_data["sala_id"],
            temperatura=validated_data["temperatura"],
            umidade=validated_data["umidade"]
        )
        return self.repository.insert(leitura)
