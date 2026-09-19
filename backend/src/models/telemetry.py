from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class LeituraSensor:
    sala_id: str
    temperatura: float
    umidade: Optional[float] = None
    id: Optional[int] = None
    data_registro: Optional[datetime] = None

    def to_dict(self):
        """Converte a entidade para dicionário serializável em JSON."""
        data = asdict(self)
        if self.data_registro:
            data["data_registro"] = self.data_registro.isoformat()
        return data
