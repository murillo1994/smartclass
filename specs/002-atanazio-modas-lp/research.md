# Phase 0: Research & Technical Decisions - Atanazio Modas LP

## 1. Paleta de Cores Claras & Design System Feminino Premium

### Contexto & Problema
A versão inicial da landing page (`atanazio-modas.html`) utilizava uma estética "dark mode" pesada (`--ink: #170B12;`, `--ink-2: #20111A;`), o que gerava baixa leitura sob luz natural no mobile, sensação de frieza e menor percepção de sofisticação para moda feminina e jeans. O usuário solicitou explicitamente clarear a página usando como referência as cores e harmonia visual da **Unic Clinic**.

### Decisão Técnica
Adotaremos o **Design System Warm Luxury**, mesclando a base neutra, clara e acolhedora da Unic Clinic com a expressividade da moda feminina e atitude da Atanazio Modas:
- **Background Principal (`--bg-page`)**: `#FAF8F5` (Creme suave Unic Clinic)
- **Superfícies & Cards (`--bg-surface`)**: `#FFFFFF` (Branco puro com sombras quentes e difusas `0 10px 30px -10px rgba(72,61,57,0.06)`)
- **Tons Neutros de Apoio**:
  - `--cream-dark`: `#F2EDE6` (fundo alternado de seções)
  - `--beige`: `#E8E0D5` (bordas sutis e divisores elegantes)
  - `--stone`: `#C4B9AD`
- **Tons de Texto e Contraste**:
  - `--text-primary`: `#2C2420` (marrom expresso escuro profundo, muito mais nobre e legível que preto puro)
  - `--text-secondary`: `#6B5446` (marrom médio para subtítulos e descrições)
  - `--text-muted`: `#9E8877` (detalhes discretos e apoios)
- **Acentos de Marca & Conversão**:
  - `--accent-gold`: `#C2935D` / `#A0765A` (dourado/terracota quente da Unic Clinic para badges, detalhes finos e estrelas de avaliação)
  - `--accent-fashion`: `#D4437B` / `#C8326E` (magenta refinado acetinado - vibrante para os botões de ação e CTAs sem poluir visualmente)
  - `--accent-denim`: `#3E5079` (azul jeans sutil para tags e indicadores de moda jeans)

### Alternativas Avaliadas
- *Fundo 100% branco frio (#FFFFFF puro em tudo)*: Rejeitado por criar aspecto genérico de e-commerce barato ou template médico frio. O tom creme `#FAF8F5` com bege `#F2EDE6` agrega sofisticação e conforto ocular.
- *Manter tons escuros*: Rejeitado por solicitação direta do usuário e menor taxa de conversão em tráfego mobile diurno.

---

## 2. Estrutura de Alta Conversão (CRO - Conversion Rate Optimization)

### Contexto & Problema
A versão anterior tinha apenas 3 botões simples, sem diferenciação de intenção de compra, sem prova social tangível (depoimentos), sem FAQ para neutralizar dúvidas e sem gatilho flutuante no mobile.

### Decisão Técnica
Implementar funil visual em 8 blocos de alta conversão:
1. **Sticky Header com Barra de Aviso Superior**:
   - Barra de anúncio superior: *"✨ Frete e Atendimento Personalizado para todo o Brasil | Loja Física em SP"*
   - Header com logo vetorizado, links de âncora e botão rápido WhatsApp com indicador online (ponto verde pulsante).
2. **Hero Section com Proposta de Valor Tripla**:
   - Título magnético e subtítulo claro.
   - 3 badges de valor imediato: *Jeans Modelador • Lingerie & Conforto • Sexy Shop com Entrega 100% Discreta*.
   - Prova social imediata (+1.500 clientes satisfeitas, 4.9 estrelas).
   - CTAs duplos: "Falar com Consultora" (WhatsApp primário) e "Ver Coleções" (rolagem suave).
3. **Vitrine dos 4 Pilares (Cards Interativos)**:
   - Jeans Modelador (foco em caimento perfeito e cintura alta).
   - Moda Feminina (looks casuais a elegantes).
   - Moda Íntima (lingeries confortáveis e rendadas).
   - Sexy Shop Discreto (sem tabu, embalagem inviolável sem identificação de conteúdo).
   - Cada card possui botão dedicado com mensagem pré-preenchida no WhatsApp direcionada à categoria.
4. **Diferenciais & Garantias de Compra**:
   - Atendimento humanizado (nada de robô frio).
   - Provador virtual assistido por fotos e medidas via WhatsApp.
   - Entrega rápida com rastreio e opção de retirada na loja física.
5. **Prova Social Tangível (Depoimentos & Avaliações Reais)**:
   - Depoimentos em cards com estrelas, foto/avatar, cidade/bairro e comentário sobre caimento e discrição.
6. **FAQ Interativo (Acordeão de Objeções)**:
   - Como funciona a escolha do tamanho?
   - As embalagens do Sexy Shop são discretas mesmo?
   - Quais as formas de pagamento aceitas?
   - Posso retirar na loja física?
   - Como funciona troca ou devolução?
7. **Localização da Loja Física & Rota**:
   - Endereço completo: Rua Ary Pereira de Lima, 403.
   - Horários, integração direta com Google Maps e botão "Como Chegar".
8. **Botão Flutuante de WhatsApp (FAB)**:
   - Fixo no canto inferior direito.
   - Balãozinho de mensagem flutuante após 4 segundos: *"Olá! Posso te ajudar a escolher sua peça?"*.
   - Pulso sutil para atrair o olhar sem ser invasivo.

---

## 3. Conformidade com a Constituição (Princípio VI: Front-End, Tracking & Performance)

### Contexto & Problema
O Princípio VI exige rastreamento dinâmico sem IDs hardcoded, atributos de dados semânticos obrigatórios (`data-track`), atributos `id` exclusivos para dataLayer e otimização severa para tráfego pago (Google PageSpeed).

### Decisão Técnica
- **Atributos Semânticos**:
  - `data-track="lead_whatsapp_header"`
  - `data-track="lead_whatsapp_hero"`
  - `data-track="lead_whatsapp_category_jeans"`
  - `data-track="lead_whatsapp_category_lingerie"`
  - `data-track="lead_whatsapp_category_sexyshop"`
  - `data-track="lead_whatsapp_floating"`
  - `data-track="faq_toggle"`
  - `data-track="maps_click"`
- **Data Layer Engine**:
  - Um script leve e nativo que escuta eventos `click` em qualquer elemento com `[data-track]`.
  - Dispara evento no `window.dataLayer = window.dataLayer || []` no formato:
    `dataLayer.push({ event: 'conversion_intent', category: 'WhatsApp', label: trackLabel, source_id: id })`
  - Se `window.fbq` estiver presente, chama `fbq('trackCustom', 'LeadWhatsApp', { label: trackLabel })`.
  - Nenhuma chave ou ID de Pixel/GTM é hardcoded; o código está pronto para receber injeção de scripts no `<head>` via GTM ou CMS.
- **Performance**:
  - Zero dependências de frameworks pesados (100% Vanilla HTML5 + CSS3 + Vanilla JS enxuto).
  - Ícones SVG inline com classes de estilo (sem requisições HTTP adicionais de icon fonts).
  - Webfonts pré-conectadas (`preconnect`) com `font-display: swap`.
  - Animações CSS por GPU (`transform`, `opacity`) com respeito a `prefers-reduced-motion`.

---

## 4. Estrutura de Arquivos & Distribuição

### Decisão
A landing page de alta conversão será gerada em `atanazio_modas/index.html` (e mantida também sincronizada como `atanazio_modas/atanazio-modas.html` para preservação e compatibilidade), permitindo servir diretamente como página estática estandarte ou ser incorporada a qualquer servidor web (Nginx, Caddy, Cloudflare Pages ou Flask estático).
