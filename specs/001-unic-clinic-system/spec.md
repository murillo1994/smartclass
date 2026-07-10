# Especificação da Funcionalidade: Visão Geral do Sistema Unic Clinic

**Branch da Funcionalidade**: `001-unic-clinic-system`  
**Criado em**: 10-07-2026  
**Status**: Rascunho  
**Entrada**: Descrição do usuário: "# 0. Visão Geral e Arquitetura (System Overview) ..."

## Cenários de Usuário e Testes *(obrigatório)*

### Caso de Uso 1 - Captação e Agendamento Autônomo de Pacientes via WhatsApp (Prioridade: P1)

O sistema interage de forma autônoma com os leads no WhatsApp, responde a dúvidas sobre os procedimentos da clínica, qualifica o interesse do paciente, verifica a grade de horários e insere agendamentos reais diretamente no banco de dados.

**Por que esta prioridade**: É a principal proposta de valor do sistema (concierge digital), liberando a equipe de recepção humana de fluxos repetitivos de agendamento e convertendo visitantes em pacientes agendados.

**Teste Independente**: Pode ser testado de ponta a ponta simulando mensagens de webhook do WhatsApp recebidas para um paciente fictício, verificando se a IA gera respostas corretas, valida a disponibilidade e cria um agendamento no banco de dados.

**Cenários de Aceitação**:

1. **Dado** que um novo lead envia uma mensagem no WhatsApp da clínica perguntando sobre um procedimento específico (ex: botox), **Quando** a mensagem for processada, **Então** o concierge digital responde com informações contextualizadas refletindo a estética premium da clínica.
2. **Dado** que um paciente solicita o agendamento de uma consulta em um dia e horário específicos, **Quando** o concierge digital chama a ferramenta de verificação de disponibilidade e encontra o horário livre, **Então** ele registra o agendamento no banco de dados e envia uma confirmação pelo WhatsApp.
3. **Dado** que um paciente solicita um horário que já está ocupado, **Quando** o concierge digital verifica a disponibilidade, **Then** ele informa o paciente de forma educada e sugere horários alternativos.

---

### Caso de Uso 2 - Painel do Recepcionista e CRM Kanban (Prioridade: P2)

O recepcionista utiliza um painel administrativo baseado em SvelteKit com um quadro Kanban para acompanhar os leads pelo funil de vendas, visualizar o histórico de conversas e intervir manualmente (ativar o handoff) quando necessário.

**Por que esta prioridade**: Necessário para que os recepcionistas supervisionem a IA, gerenciem a progressão dos leads e tratem de exceções onde a intervenção humana é necessária.

**Teste Independente**: Pode ser testado carregando o painel de controle, arrastando um card de lead para outra coluna, abrindo a visualização do chat e alternando o botão "Handoff".

**Cenários de Aceitação**:

1. **Dado** que um novo lead inicia uma conversa no WhatsApp, **Quando** o lead é cadastrado, **Então** ele aparece na primeira coluna ("Novo Lead") do painel Kanban em tempo real.
2. **Dado** que um lead precisa de atenção humana personalizada, **Quando** o recepcionista clica em "Handoff" na visualização do chat, **Então** a IA é pausada para aquele lead e todas as mensagens recebidas e enviadas são marcadas como gerenciadas por humano.
3. **Dado** que o recepcionista envia uma mensagem pela janela de chat do painel, **Quando** enviada, **Então** a mensagem é enviada ao lead através da instância de WhatsApp da Evolution API.

---

### Caso de Uso 3 - Site Institucional Premium (Prioridade: P3)

Uma página de destino (landing page) de alto desempenho que representa a estética boutique da Unic Clinic, desenhada para capturar a atenção do visitante e direcioná-lo para iniciar uma conversa no WhatsApp.

**Por que esta prioridade**: O ponto de entrada para o tráfego online (anúncios pagos), essencial para converter visitantes em leads.

**Teste Independente**: Pode ser testado carregando a landing page e verificando o design, o desempenho e o redirecionamento para o WhatsApp.

**Cenários de Aceitação**:

1. **Dado** que um usuário abre a URL da landing page, **Quando** a página é carregada, **Então** ela exibe uma estilização de alta qualidade, tipografia personalizada e microanimações suaves.
2. **Dado** que um usuário clica no botão de chamada para ação "Agendar Consulta", **Quando** clicado, **Então** ele é redirecionado para o WhatsApp com uma mensagem de boas-vindas pré-configurada.

---

### Casos de Borda (Edge Cases)

- **Instabilidade/Queda da API da OpenAI**: Se a API da OpenAI falhar, o backend deve retornar uma mensagem amigável padrão (ex: "Desculpe, estou com uma instabilidade. Um de nossos atendentes irá falar com você em breve.") e sinalizar o lead no CRM para intervenção manual.
- **Reserva Dupla (Overbooking)**: Se dois pacientes tentarem agendar o mesmo horário simultaneamente, a transação ou restrições do banco de dados devem impedir a duplicidade, exibindo o erro de forma amigável no fluxo do segundo paciente.
- **Mensagens de Mídia/Áudio**: Se um paciente enviar uma mensagem de áudio ou imagem, o sistema deve notificar o recepcionista para triagem manual ou tentar transcrever (se o Whisper estiver ativo) ou pedir educadamente que envie texto.

## Requisitos *(obrigatório)*

### Requisitos Funcionais

- **RF-001**: O sistema DEVE processar webhooks de entrada da Evolution API referentes à instância `unic_clinic`.
- **RF-002**: O sistema DEVE integrar-se à API da OpenAI utilizando Function Calling para permitir que a IA consulte/reserve horários e gerencie detalhes do lead.
- **RF-003**: O sistema DEVE expor uma grade de agendamento verificando a disponibilidade em tempo real no PostgreSQL.
- **RF-004**: O sistema DEVE fornecer um painel CRM baseado em SvelteKit com colunas de etapas Kanban para os leads.
- **RF-005**: O sistema DEVE suportar um mecanismo de "Handoff" para pausar o agente de IA quando um recepcionista assumir o controle manual.
- **RF-006**: O sistema DEVE persistir todas as informações de pacientes, histórico de mensagens, procedimentos e agendamentos no PostgreSQL.
- **RF-007**: O sistema DEVE renderizar um site institucional premium e minimalista, otimizado para carregamento rápido e com identidade visual de marca boutique.

### Entidades Chave *(incluir se a funcionalidade envolver dados)*

- **Paciente (Lead)**: Representa o cliente. Campos: ID, Nome, Telefone, Etapa Kanban (Novo, Qualificado, Agendado, Sem Interesse), Status da IA (Ativa/Pausada).
- **Mensagem**: Representa uma mensagem do chat. Campos: ID, ID do Paciente, Remetente (Paciente, IA, Agente), Conteúdo de Texto, Data/Hora.
- **Procedimento**: Representa os serviços oferecidos. Campos: ID, Nome, Descrição, Duração, Preço.
- **Agendamento**: Representa uma consulta reservada. Campos: ID, ID do Paciente, ID do Procedimento, Horário de Início, Horário de Fim, Status (Confirmado, Concluído, Cancelado).

## Critérios de Sucesso *(obrigatório)*

### Resultados Mensuráveis

- **CS-001**: Pacientes devem conseguir concluir o fluxo de agendamento de forma autônoma no WhatsApp em menos de 3 minutos.
- **CS-002**: O painel do SvelteKit deve atualizar em tempo real quando novas mensagens chegarem via webhook ou os leads mudarem de etapa.
- **CS-003**: O site institucional deve carregar em menos de 1,5 segundos em conexões móveis padrão.
- **CS-004**: O sistema deve processar o webhook do WhatsApp de entrada e disparar a resposta da IA em menos de 3 segundos.

## Premissas

- Temos acesso completo a uma instância funcional da Evolution API executando no mesmo servidor VPS ou acessível localmente.
- O banco de dados PostgreSQL funcionará como um contêiner Docker `unic_db` e será persistente.
- As credenciais da API da OpenAI (Chave de API) estão disponíveis e são válidas.
