import logging
from typing import Optional, List
from src.database import get_db_connection
from src.models.telemetry import LeituraSensor

logger = logging.getLogger(__name__)

class TelemetryRepository:
    """Repositório de persistência para leituras de telemetria no PostgreSQL."""

    def insert(self, leitura: LeituraSensor) -> LeituraSensor:
        """Insere uma nova leitura de forma imutável e retorna a entidade com ID e timestamp."""
        query = """
        INSERT INTO leitura_sensores (sala_id, temperatura, umidade)
        VALUES (%s, %s, %s)
        RETURNING id, sala_id, temperatura, umidade, data_registro;
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        query,
                        (
                            leitura.sala_id,
                            leitura.temperatura,
                            leitura.umidade
                        )
                    )
                    row = cur.fetchone()
                    conn.commit()

                    if row:
                        return LeituraSensor(
                            id=row[0],
                            sala_id=row[1],
                            temperatura=float(row[2]),
                            umidade=float(row[3]) if row[3] is not None else None,
                            data_registro=row[4]
                        )
                    raise RuntimeError("Falha ao recuperar o registro recém-inserido.")
        except Exception as e:
            logger.error(f"Erro na camada de repositório ao inserir telemetria: {e}")
            raise

    def find_by_id(self, reading_id: int) -> Optional[LeituraSensor]:
        """Recupera uma leitura específica pelo ID primário."""
        query = """
        SELECT id, sala_id, temperatura, umidade, data_registro
        FROM leitura_sensores
        WHERE id = %s;
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (reading_id,))
                    row = cur.fetchone()
                    if row:
                        return LeituraSensor(
                            id=row[0],
                            sala_id=row[1],
                            temperatura=float(row[2]),
                            umidade=float(row[3]) if row[3] is not None else None,
                            data_registro=row[4]
                        )
                    return None
        except Exception as e:
            logger.error(f"Erro na camada de repositório ao buscar telemetria id={reading_id}: {e}")
            raise

    def list_recent(self, limit: int = 50) -> List[LeituraSensor]:
        """Retorna as leituras mais recentes ordenadas por timestamp decrescente."""
        query = """
        SELECT id, sala_id, temperatura, umidade, data_registro
        FROM leitura_sensores
        ORDER BY data_registro DESC
        LIMIT %s;
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (limit,))
                    rows = cur.fetchall()
                    return [
                        LeituraSensor(
                            id=row[0],
                            sala_id=row[1],
                            temperatura=float(row[2]),
                            umidade=float(row[3]) if row[3] is not None else None,
                            data_registro=row[4]
                        )
                        for row in rows
                    ]
        except Exception as e:
            logger.error(f"Erro na camada de repositório ao listar telemetrias recentes: {e}")
            raise
