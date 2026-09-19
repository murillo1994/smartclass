# Data Model: API de Ingestão de Dados IoT (Módulo 1)

**Feature**: API de Ingestão de Dados IoT (Módulo 1)  
**Branch**: `003-iot-telemetry-ingestion`  
**Date**: 2026-09-13  

---

## 1. Entidades Relacionais

### Tabela: `leitura_sensores`

Armazena as medições brutas e imutáveis coletadas pelos módulos de sensoriamento instalados nas salas de aula.

| Coluna | Tipo SQL | Restrições / Modificadores | Descrição |
|---|---|---|---|
| `id` | `SERIAL` (ou `BIGSERIAL`) | `PRIMARY KEY` | Identificador único sequencial do registro de telemetria |
| `sala_id` | `VARCHAR(50)` | `NOT NULL` | Identificador ou rótulo da sala de aula monitorada (ex: `"Sala 101"`, `"Lab 02"`) |
| `temperatura` | `DECIMAL(5,2)` | `NOT NULL` | Valor da temperatura medida em graus Celsius (°C) |
| `umidade` | `DECIMAL(5,2)` | `NULL` | Valor opcional da umidade relativa do ar em porcentagem (%) |
| `data_registro` | `TIMESTAMP WITH TIME ZONE` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Data e hora da inserção no banco de dados (tempo controlado pelo servidor) |

---

## 2. Índices e Otimizações de Acesso

1. **Índice Primário**: `PRIMARY KEY (id)` — B-Tree padrão para buscas e referências pontuais.
2. **Índice Temporal por Sala (para consultas analíticas e médias futuras)**:
   ```sql
   CREATE INDEX IF NOT EXISTS idx_leitura_sensores_sala_data 
   ON leitura_sensores (sala_id, data_registro DESC);
   ```

---

## 3. Regras de Integridade e Validação

1. **Imutabilidade**:
   - Registros na tabela `leitura_sensores` são do tipo *append-only*.
   - Operações de `UPDATE` e `DELETE` são terminantemente proibidas na aplicação operacional para preservar o histórico.

2. **Validação de Domínio dos Dados**:
   - `sala_id`: String não vazia, comprimento entre 1 e 50 caracteres (sem espaços em branco isolados).
   - `temperatura`: Valor decimal entre `-40.00` e `85.00` °C (faixa operacional padrão de sensores como DHT11, DHT22 ou DS18B20).
   - `umidade`: Se informada, valor decimal entre `0.00` e `100.00` %. Se omitida, valor persistido como `NULL`.
   - `data_registro`: Gerado estritamente pela função `CURRENT_TIMESTAMP` do PostgreSQL.

---

## 4. Esquema DDL (PostgreSQL)

```sql
-- DDL de Criação da Tabela de Telemetria
CREATE TABLE IF NOT EXISTS leitura_sensores (
    id SERIAL PRIMARY KEY,
    sala_id VARCHAR(50) NOT NULL,
    temperatura DECIMAL(5,2) NOT NULL,
    umidade DECIMAL(5,2),
    data_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Índice para otimização de consultas temporais por ambiente
CREATE INDEX IF NOT EXISTS idx_leitura_sensores_sala_data 
ON leitura_sensores (sala_id, data_registro DESC);
```
