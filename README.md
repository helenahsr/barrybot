# Barry BOT

## Sobre o Projeto

Este é um bot simples, mas poderoso, para o Discord, projetado para otimizar o fluxo de trabalho de suporte e gerenciamento de tarefas. Ele integra a comunicação da equipe em um canal do Discord com um quadro Kanban no Trello, transformando automaticamente tópicos de discussão em cartões de tarefa.

### Funcionalidades
- Criação Automática de Tickets: Cria um novo card no Trello sempre que um tópico é aberto no canal de suporte do Discord.
- Atualização de Status (Emojis): Adiciona automaticamente o emoji 🟡 no nome do tópico quando o ticket é criado, indicando que a tarefa está "em andamento".
  - Comando de Resolução: Usa o comando `!resolvido` para:
  - Mudar o emoji do tópico para 🟢, indicando que a tarefa foi concluída.
  - Trancar o tópico, impedindo novas mensagens.
  - Arquivar o tópico, movendo-o para a seção de tópicos encerrados.
- Integração com o Trello: O bot captura o título do tópico e o conteúdo da primeira mensagem para popular os detalhes do card no Trello.

### Tecnologias Utilizadas
- Python: Linguagem principal para o desenvolvimento do bot.
- `discord.py`: Biblioteca para interação com a API do Discord.
- `py-trello`: Biblioteca para interação com a API do Trello.
- `python-dotenv`: Para gerenciar variáveis de ambiente de forma segura.

## Configuração (Setup)

**1. Pré-requisitos**

Certifique-se de ter o Python instalado e o pip configurado.

**2. Obtenha as Credenciais**

Você precisará de três conjuntos de credenciais:
- Discord:
  - Token do Bot
  - ID do Canal de Suporte
  - ID do Cargo de Suporte (@TI - Suporte)

- Trello:
  - Sua Chave de API (API Key)
  - Seu Token de API
  - ID do Quadro Kanban
  - ID da Lista "Backlog"

Siga as instruções nas páginas de desenvolvedor do Discord e do Trello para obter esses IDs.

**3. Crie o Arquivo .env**

Na raiz do seu projeto, crie um arquivo chamado .env (com o ponto na frente) e adicione suas credenciais nele.

```
DISCORD_TOKEN='SEU_TOKEN_DO_DISCORD'
TRELLO_API_KEY='SUA_CHAVE_DE_API_DO_TRELLO'
TRELLO_API_TOKEN='SEU_TOKEN_DE_API_DO_TRELLO'
TRELLO_BOARD_ID='ID_DO_SEU_QUADRO'
TRELLO_BACKLOG_LIST_ID='ID_DA_SUA_LISTA_BACKLOG'
SUPORTE_CHANNEL_ID='ID_DO_CANAL_DE_SUPORTE'
SUPORTE_ROLE_ID='ID_DO_CARGO_DE_SUPORTE'
```

**4. Instale as Dependências**

Abra seu terminal na pasta do projeto e execute:
Bash

```
pip install -r requirements.txt
```

Se você ainda não tem um arquivo requirements.txt, pode criá-lo com:

```
pip install discord.py python-dotenv trello
pip freeze > requirements.txt 
```

## Como Usar o Bot

**1. Inicie o Bot**

Execute o script principal a partir do seu terminal:

```
python bot.py
```

**2. Crie um Ticket**

Vá para o canal de suporte (#chame-ti-suporte) no Discord e crie um novo tópico. O bot irá automaticamente:
- Adicionar o emoji 🟡 ao nome do tópico.
- Criar um card no Trello com o título e a descrição da sua mensagem.
- Responder no tópico com o link para o card.

**3. Resolva um Ticket**
Quando a tarefa estiver concluída, vá para o tópico correspondente e digite o comando:
`!resolvido`

O bot irá:
- Mudar o emoji do tópico para 🟢.
- Trancar e arquivar o tópico.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE.md para detalhes.
