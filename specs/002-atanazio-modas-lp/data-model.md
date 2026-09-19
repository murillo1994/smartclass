# Phase 1: Data Model & Component Schema - Atanazio Modas LP

## 1. Modelo de Componentes da Interface (UI Component Model)

A Landing Page é estruturada em blocos modulares semanticamente demarcados:

```
[Announcement Bar] -> Aviso de frete e atendimento
       │
[Sticky Header] -> Logo + Navegação + CTA Rápido (Online Status)
       │
[Hero Section] -> UVP + Badges de Confiança + Prova Social Rápida + CTAs Duplos
       │
[Category Pillars] -> 4 Vitrines (Jeans Modelador, Moda Feminina, Lingerie, Sexy Shop)
       │
[Guarantees & Diferenciais] -> Atendimento consultivo, prova assistida, discrição
       │
[Social Proof (Depoimentos)] -> 3 a 4 avaliações reais de clientes com notas e fotos
       │
[Interactive FAQ] -> 5 acordes de quebra de objeções
       │
[Physical Store & Location] -> Endereço, mapa interativo, horário e rota
       │
[Footer] -> Contatos, redes sociais, políticas e direitos
       │
[Floating WhatsApp CTA] -> Botão com pulso e balão de mensagem persuasivo
```

---

## 2. Estrutura de Dados dos Componentes

### 2.1. Categoria da Vitrine (`CategoryCard`)
| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `id` | String | Identificador único do elemento | `"cat-jeans"` |
| `title` | String | Título da categoria | `"Jeans Modelador"` |
| `tagline` | String | Descrição curta de valor | `"Cintura perfeita, tecnologia levanta bumbum"` |
| `badge` | String | Destaque promocional | `"Mais Vendido"` |
| `whatsapp_msg` | String | Mensagem pré-formatada para URL | `"Olá! Quero conhecer os modelos de Jeans Modelador no meu tamanho."` |
| `track_id` | String | Atributo `data-track` | `"lead_whatsapp_cat_jeans"` |

### 2.2. Depoimento de Cliente (`Testimonial`)
| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `name` | String | Nome da cliente | `"Camila R."` |
| `location` | String | Cidade/Bairro | `"São Paulo - SP"` |
| `rating` | Number | Avaliação em estrelas | `5` |
| `comment` | String | Texto do depoimento | `"O jeans veste perfeito e não aperta na cintura! Chegou super rápido e o atendimento foi nota 10."` |
| `verified_purchase` | Boolean | Tag de compradora verificada | `true` |

### 2.3. Pergunta Frequente (`FaqItem`)
| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `question_id` | String | ID para rastreio e acessibilidade | `"faq-1"` |
| `question` | String | Pergunta da cliente | `"Como escolho o tamanho certo pelo WhatsApp?"` |
| `answer` | String | Resposta acolhedora e explicativa | `"Nossa consultora envia a tabela de medidas detalhada e te orienta em tempo real..."` |

---

## 3. Esquema de Rastreamento e Conversão (Data Layer Contract)

Em estrito atendimento ao **Princípio VI da Constituição**:

```typescript
interface TrackingEvent {
  event: "conversion_intent" | "interaction";
  category: "WhatsApp" | "FAQ" | "Navigation" | "Location";
  action: "click" | "toggle" | "scroll";
  label: string;          // Ex: "hero_primary_cta", "cat_sexyshop", "floating_btn"
  source_id: string;      // ID único do elemento HTML (ex: "btn-hero-wa")
  timestamp: number;      // Epoch ms
  page_location: string;  // window.location.href
}
```
