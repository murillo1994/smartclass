import logging
from contextlib import contextmanager
import psycopg2
from psycopg2 import pool
from src.config import Config

logger = logging.getLogger(__name__)

_pool = None

def init_pool():
    """Inicializa o pool de conexões thread-safe com PostgreSQL."""
    global _pool
    if _pool is None:
        try:
            if Config.DATABASE_URL:
                _pool = psycopg2.pool.ThreadedConnectionPool(
                    minconn=1,
                    maxconn=20,
                    dsn=Config.DATABASE_URL
                )
            else:
                _pool = psycopg2.pool.ThreadedConnectionPool(
                    minconn=1,
                    maxconn=20,
                    host=Config.POSTGRES_HOST,
                    port=Config.POSTGRES_PORT,
                    database=Config.POSTGRES_DB,
                    user=Config.POSTGRES_USER,
                    password=Config.POSTGRES_PASSWORD
                )
            logger.info("Pool de conexões PostgreSQL inicializado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao inicializar pool de conexões PostgreSQL: {e}")
            _pool = None
            raise

def get_pool():
    """Retorna o pool de conexões ativo, inicializando se necessário."""
    global _pool
    if _pool is None:
        init_pool()
    return _pool

@contextmanager
def get_db_connection():
    """Context manager para obter e liberar conexões do pool de forma segura."""
    p = get_pool()
    conn = p.getconn()
    try:
        yield conn
    finally:
        if p and conn:
            p.putconn(conn)

def init_db():
    """Executa DDL idempotente para criar tabelas e índices de telemetria."""
    ddl_statement = """
    CREATE TABLE IF NOT EXISTS leitura_sensores (
        id SERIAL PRIMARY KEY,
        sala_id VARCHAR(50) NOT NULL,
        temperatura DECIMAL(5,2) NOT NULL,
        umidade DECIMAL(5,2),
        data_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
    );

    CREATE INDEX IF NOT EXISTS idx_leitura_sensores_sala_data 
    ON leitura_sensores (sala_id, data_registro DESC);
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(ddl_statement)
                conn.commit()
        logger.info("Tabela 'leitura_sensores' e índices verificados/inicializados com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao inicializar schema do banco de dados: {e}")
        # Não trava a inicialização caso o banco ainda esteja subindo, mas loga erro
        raise
