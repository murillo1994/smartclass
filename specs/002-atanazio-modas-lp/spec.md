# Feature Specification: Landing Page de Alta Conversão - Atanazio Modas

**Feature Branch**: `002-atanazio-modas-lp`  
**Created**: 2026-08-30  
**Status**: Draft  
**Input**: User description: "quero criar uma landing page de alta conversão para a atanazio modas, temos na pasta um html como referencia, porém temos que melhorar, inclusive achei muito escuro quero trazer cores mais claras podemos usar como refrencia também as cores da unic clinic"

## Visão Geral e Contexto

A Atanazio Modas atua com moda feminina, moda íntima, sexy shop e jeans modelador, possuindo loja física em Guarulhos - SP (Rua Ary Pereira de Lima, 403) e atendimento comercial ativo via WhatsApp (11 97231-2358).
A referência anterior contida em `atanazio_modas/atanazio-modas.html` possuía tom excessivamente escuro (`--ink: #170B12`), pouca quebra visual para leitura móvel e elementos limitados de conversão direta.

Esta especificação define a reformulação completa para uma **Landing Page de Alta Conversão (CRO)**, migrando para uma paleta clara, sofisticada e acolhedora inspirada nos tons quentes e premium da Unic Clinic (tons de creme `#faf8f5`, bege `#f2ede6`, branco quente `#ffffff`, detalhes terracota/dourado suave `#a0765a` e toques refinados de magenta/blush acetinado `#c84271`), mantendo a sensualidade, atitude e elegância da marca sem pesar a atmosfera visual.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Descoberta e Conversão Imediata no WhatsApp (Priority: P1)

Como uma cliente que chegou via anúncio (Meta Ads ou Google Ads) procurando jeans modelador ou lingerie, quero visualizar instantaneamente o diferencial da Atanazio Modas, sua proposta de valor em ambiente claro e sofisticado, e clicar para iniciar atendimento personalizado no WhatsApp com mensagem contextualizada da peça/categoria.

**Why this priority**: É o objetivo primário de negócio da landing page (conversão de tráfego pago e orgânico em conversas qualificadas de vendas no WhatsApp).

**Independent Test**: Pode ser validado abrindo a página, verificando tempo de carregamento inferior a 1.5s, visualizando o hero com contraste claro impecável e clicando em qualquer CTA de WhatsApp, verificando o redirecionamento com mensagem pré-definida e evento de data-layer disparado.

**Acceptance Scenarios**:
1. **Given** que a usuária acessa a página em dispositivo móvel, **When** visualiza o Hero acima da dobra, **Then** encontra título de impacto, prova social (avaliações/seguidores), fotos em tons claros e botão de destaque para o WhatsApp.
2. **Given** que a usuária clica no botão principal "Falar com Consultora no WhatsApp", **When** o app do WhatsApp abre, **Then** o link carrega com mensagem inicial sugerida (ex: *"Olá! Vi o site da Atanazio Modas e gostaria de conhecer as novidades."*).

---

### User Story 2 - Exploração de Categorias e Catálogo Dinâmico (Priority: P2)

Como uma visitante interessada em peças específicas (Jeans que modela, Moda Feminina Casual/Chic, Moda Íntima/Lingerie ou Sexy Shop Discreto), quero navegar por cards visuais organizados e convidativos, entendendo os diferenciais de cada linha e clicando para solicitar catálogo ou fotos específicas no WhatsApp.

**Why this priority**: Segmenta os interesses de compra das clientes, permitindo que o atendimento no WhatsApp já saiba exatamente se o interesse é jeans, lingerie ou produtos íntimos sensuais.

**Independent Test**: Clicar no card de "Sexy Shop" e verificar mensagem específica: *"Olá! Gostaria de ver o catálogo discreto de Sexy Shop"*; clicar no card de "Jeans" e receber mensagem específica sobre numerações e modelos.

**Acceptance Scenarios**:
1. **Given** a seção de categorias com design clean e moderno, **When** a cliente seleciona uma categoria, **Then** visualiza fotos inspiracionais com acabamento leve e botões individuais de pedido/catálogo.
2. **Given** a categoria de Sexy Shop, **When** a visitante acessa, **Then** há destaque explícito para "Atendimento 100% Discreto & Embalagem sem Identificação Externa", reduzindo fricção e tabu de compra.

---

### User Story 3 - Quebra de Objeções, Prova Social e Localização da Loja (Priority: P3)

Como uma cliente nova que nunca comprou na Atanazio Modas, quero ver depoimentos reais, garantia de atendimento seguro, FAQ para sanar dúvidas (tamanhos, formas de pagamento, trocas, entrega) e detalhes da loja física em Guarulhos - SP (endereço, mapa e horário) para sentir total segurança antes de comprar.

**Why this priority**: Aumenta significativamente a taxa de conversão (CRO), reduzindo abandono e objeções comuns de e-commerce e vendas por WhatsApp.

**Independent Test**: Interagir com o FAQ accordion, checar o mapa interativo/link do Google Maps e ler os depoimentos de clientes satisfeitas.

**Acceptance Scenarios**:
1. **Given** a seção de FAQ interativo, **When** o usuário clica em uma pergunta sobre troca ou entrega, **Then** o accordion expande suavemente com a resposta clara e objetiva.
2. **Given** o card da loja física, **When** a visitante clica em "Ver rota no Google Maps", **Then** é redirecionada para a localização precisa no Google Maps (Rua Ary Pereira de Lima, 403).

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A Landing Page DEVE ser implementada com paleta de cores clara, luminosa e elegante baseada nos tons da Unic Clinic (fundo principal em tom creme/off-white `--cream: #faf8f5`, superfícies em branco quente `#ffffff`, acentos secundários em bege/terracota suave e detalhes de ação em magenta sofisticado/framboesa `--rose-accent: #c84271`).
- **FR-002**: A página DEVE possuir Header fixo (*sticky*) com logotipo da Atanazio Modas, links de rolagem suave para as seções e CTA rápido para o WhatsApp.
- **FR-003**: O Hero DEVE apresentar Proposta Única de Valor (UVP), badges de confiança ("Loja Física em SP", "Envio para todo o Brasil", "Atendimento Humanizado"), botões primário e secundário de ação, e bloco de métricas/estatísticas de satisfação.
- **FR-004**: A seção de Coleções DEVE conter 4 pilares bem definidos: (1) Jeans Modelador & Premium, (2) Moda Feminina Autoral, (3) Moda Íntima & Lingerie, (4) Sexy Shop com Discrição Total.
- **FR-005**: Todo botão de CTA para o WhatsApp DEVE incluir um link `https://wa.me/5511972312358?text=...` com mensagem personalizada de acordo com a seção de origem.
- **FR-006**: DEVE existir um botão flutuante de WhatsApp fixo no canto inferior direito da tela, com animação sutil de pulso e balão de mensagem convidativo após alguns segundos de navegação.
- **FR-007**: A página DEVE incluir seção de Avaliações / Prova Social com depoimentos de clientes (estrelas, comentários, fotos de looks e menção ao conforto das peças).
- **FR-008**: A página DEVE incluir um Acordeão de Dúvidas Frequentes (FAQ) com respostas para as 5 principais objeções de compra.
- **FR-009**: A página DEVE conter seção institucional com endereço da loja física, horário de funcionamento, link para Google Maps e canais oficiais de contato.
- **FR-010**: Em estrita conformidade com o **Princípio VI da Constituição**:
  - Todo elemento clicável (botões, CTAs, links de saída, acordeões) DEVE possuir um `id` exclusivo e atributo de tracking semântico (ex: `data-track="lead_whatsapp_hero"`, `data-track="faq_expand"`).
  - O código DEVE conter script modular de Data Layer preparado para disparar eventos para Google Tag Manager (`dataLayer.push`) e Meta Pixel (`fbq('track', ...)`), sem IDs de contas hardcoded.
  - As imagens e assets pesados DEVEM utilizar `loading="lazy"` e atributos modernos de dimensionamento e otimização.

---

### Non-Functional & Visual Design Requirements

- **NFR-001 (Performance)**: Carregamento do First Contentful Paint (FCP) < 1.0s e Largest Contentful Paint (LCP) < 1.8s em conexões 4G mobile.
- **NFR-002 (Responsividade)**: Design Mobile-First testado e fluido para viewports de 360px a 1920px.
- **NFR-003 (Acessibilidade)**: Contraste de texto conforme diretrizes WCAG AA sobre fundo claro.
- **NFR-004 (Tipografia)**: Combinação moderna entre tipografia editorial de títulos (ex: *Playfair Display* ou *Unbounded/Syne* em pesos equilibrados) e tipografia neutra altamente legível para corpo de texto (*Plus Jakarta Sans* ou *Manrope*).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Pontuação do Google PageSpeed Insights >= 90 tanto no Mobile quanto no Desktop.
- **SC-002**: 100% dos cliques em CTAs registram eventos semânticos no console e no `dataLayer` com metadados do botão.
- **SC-003**: Redução da percepção de peso visual em 100% através da substituição do fundo escuro por paleta clara e arejada com estética premium.
- **SC-004**: Taxa esperada de conversão (CTR para WhatsApp) >= 8% do tráfego qualificado de visitantes.

