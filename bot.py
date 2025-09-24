import os
import discord
from dotenv import load_dotenv
from trello import TrelloClient
from discord.ext import commands

# carrega as variáveis de ambiente do .env
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_API_TOKEN = os.getenv('TRELLO_API_TOKEN')
TRELLO_BOARD_ID = os.getenv('TRELLO_BOARD_ID')
TRELLO_BACKLOG_LIST_ID = os.getenv('TRELLO_BACKLOG_LIST_ID')
SUPORTE_CHANNEL_ID = int(os.getenv('SUPORTE_CHANNEL_ID'))
SUPORTE_ROLE_ID = os.getenv('SUPORTE_ROLE_ID')

# configura o bot do Discord com o prefixo de comando
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# conecta na API do Trello
trello_client = TrelloClient(
    api_key=TRELLO_API_KEY,
    token=TRELLO_API_TOKEN
)

# evento para quando o bot estiver online
@bot.event
async def on_ready():
    print(f'Bot está conectado como {bot.user}')
    print('Barrybot pronto para monitorar a criação de tópicos!')

# evento para quando um tópico é criado
@bot.event
async def on_thread_create(thread):
    # valida se o tópico foi criado no canal de suporte correto
    if thread.parent_id != SUPORTE_CHANNEL_ID:
        return

    print(f'Novo tópico "{thread.name}" criado no canal de suporte.')

    # Pega a primeira mensagem do tópico para obter o conteúdo original
    # primeira_mensagem = None
    async for message in thread.history(limit=1, oldest_first=True):
        print(message)
        # primeira_mensagem = message
        break

    # Se a primeira mensagem for encontrada, processa o conteúdo e edita o nome do tópico para adicionar o circulo amarelo
    novo_nome_topico = f"🟡 {thread.name}"
    await thread.edit(name=novo_nome_topico)
    print(f'Nome do tópico editado para "{novo_nome_topico}".')

        # verifica se a mensagem tem a menção ao cargo de @TI - Suporte
    # descricao_card = None
    # mencao_string = f"<@&{SUPORTE_ROLE_ID}>"

    # if mencao_string in descricao_card:
        # descricao_card = descricao_card.replace(mencao_string, '').strip()
    #     print('Menção ao cargo de suporte encontrada.')
    # else:
    #     descricao_card = 'Chamado criado sem menção de suporte.'
    #     print('Menção ao cargo de suporte NÃO encontrada.')

        # cria o card no Trello
    try:
        backlog_list = trello_client.get_list(TRELLO_BACKLOG_LIST_ID)
            
        new_card = backlog_list.add_card(
            name=novo_nome_topico,
            # desc=f"Criado por: {primeira_mensagem.author.name}\n\nDescrição:\n{descricao_card}"
        )
            
            # adiciona o link do tópico à descrição do card
        new_card.set_description(f"Link do Tópico: {thread.jump_url}\n\n{new_card.description}")
            
        await thread.send(f"✅ Chamado **'{new_card.name}'** criado no Trello! Link: {new_card.url}")
            
    except Exception as e:
        await thread.send(f"❌ Ocorreu um erro ao criar o chamado no Trello: {e}")


# comando para marcar o tópico como resolvido
@bot.command(name='resolvido')
async def resolvido(ctx):
    # verifica se o comando foi usado dentro de um tópico
    if not isinstance(ctx.channel, discord.Thread):
        await ctx.send("Este comando só pode ser usado em um tópico.")
        return
    
    thread = ctx.channel

    emojis_de_status = ['🟡', '🟢', '🔴', '🟣']
    
    nome_topico_limpo = thread.name
    
    # verifica se o nome do tópico começa com algum dos emojis da lista
    for emoji in emojis_de_status:
        if nome_topico_limpo.startswith(emoji):
            nome_topico_limpo = nome_topico_limpo[len(emoji):].lstrip()
            break
    
    # edita o nome do tópico para adicionar a bolinha verde
    novo_nome_topico = f"🟢 {nome_topico_limpo}"
    await thread.edit(name=novo_nome_topico, locked=True, archived=True)
    
    await ctx.send(f"✅ O tópico foi marcado como resolvido e encerrado!")

# comando para passar o tópico para a Diretoria de TI
@bot.command(name='direcao')
async def direcao(ctx):
    # verifica se o comando foi usado dentro de um tópico
    if not isinstance(ctx.channel, discord.Thread):
        await ctx.send("Este comando só pode ser usado em um tópico.")
        return
    
    thread = ctx.channel
    
    # edita o nome do tópico para adicionar a bolinha vermelha
    novo_nome_topico = f"🔴 {thread.name.lstrip('🟡 ')}"
    await thread.edit(name=novo_nome_topico)
    
    await ctx.send(f"✅ O tópico foi passado para a Diretoria de TI!")

# inicia o bot
bot.run(DISCORD_TOKEN)