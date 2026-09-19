# Data Model: Dashboard Web de Monitoramento das Salas de Aula (Módulo 2)

**Feature**: Dashboard Web de Monitoramento das Salas de Aula (Módulo 2)  
**Branch**: `004-classroom-dashboard`  
**Date**: 2026-09-13  

---

## 1. Estruturas de Dados do Frontend (Estado da Aplicação)

### `DashboardState` (Estado Global da Interface)

```typescript
interface DashboardState {
  isConnected: boolean;               // Indica se a última chamada à API foi bem-sucedida
  lastUpdated: Date | null;           // Horário da última atualização dos dados
  autoRefreshInterval: number;        // Intervalo em ms (0 = desativado, 5000, 10000, 30000)
  selectedRoomFilter: string;         // Filtro de sala selecionado ("all" ou nome da sala)
  rawReadings: TelemetriaItem[];      // Lista de leituras retornadas da API
  roomSummaries: Map<string, SalaResumo>; // Mapa de resumos agregados por sala de aula
}
```

### `SalaResumo` (Resumo Calculado por Ambiente)

```typescript
interface SalaResumo {
  sala_id: string;
  ultima_temperatura: number;
  ultima_umidade: number | null;
  data_ultima_leitura: string;
  media_temperatura: number;
  media_umidade: number | null;
  status_conforto: 'ideal' | 'quente' | 'frio' | 'atencao';
  status_badge: {
    label: string;
    bg_class: string;
    text_class: string;
    icon: string;
  };
  historico_recente: TelemetriaItem[];
}
```

### `TelemetriaItem` (Objeto de Leitura Retornado da API)

```typescript
interface TelemetriaItem {
  id: number;
  sala_id: string;
  temperatura: number;
  umidade: number | null;
  data_registro: string; // ISO 8601 UTC
}
```

---

## 2. Regras de Classificação de Conforto Térmico

| Faixa de Temperatura | Classificação | Status Visual | Ação Recomendada |
|---|---|---|---|
| `< 19.5 °C` | **Frio / Baixa Temperatura** | 🔵 Azul (`sky-500`) | Reduzir potência de climatizadores |
| `19.5 °C` a `24.5 °C` | **Confortável / Ideal** | 🟢 Verde (`emerald-500`) | Nenhuma (ambiente em condições ótimas) |
| `24.6 °C` a `27.0 °C` | **Atenção / Aquecido** | 🟡 Âmbar (`amber-500`) | Ligar ventiladores ou ventilação natural |
| `> 27.0 °C` | **Calor Excessivo** | 🔴 Vermelho (`rose-500`) | Ligar ar-condicionado e verificar ventilação |

---

## 3. Formatação e Apresentação Temporal

- Os timestamps recebidos em formato ISO 8601 UTC são convertidos no navegador para o fuso horário local (`pt-BR`):
  - Formato curto para gráficos: `HH:mm:ss`
  - Formato completo para tabela: `DD/MM/AAAA às HH:mm:ss`
