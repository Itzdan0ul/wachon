# Author: Itzdan0ul & Parrot14 (2022)
# index.py

import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from python_aternos import Client
from discord.ui import View, Button

load_dotenv()

TOKEN: str = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.emojis = True

bot = commands.Bot(command_prefix='->', intents=intents, help_command=None)

@bot.event
async def on_ready():
  print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
  if isinstance(error, commands.CommandNotFound):
    messages: list = [
      '*¡Ese comando no existe, cabrón!*', 
      '*Aún estoy pensando en más mamadas para hacer. Espera...*',
      '*¿Qué hace ese payaso todavía ahí?*',
      '*¡Qué puto pendejo estúpido!*',
      '*No sabes ni que hacer con tu vida y estás aquí diciendo tonterías.*'
    ]
    await ctx.send(messages[random.randint(0, len(messages) - 1)])
  else:
    raise error

@bot.command(name='help')
async def help(ctx: commands.Context):
  embed = discord.Embed(
    title='Comandos', 
    description='''
    Lista de comandos disponibles.
    
    **El prefijo es `->`.*

    `help` - Muestra la lista de comandos disponibles.
    `mc [OPCIÓN]` - Muestra la lista de servidores disponibles del servidor de Minecraft.

    ''', 
    color=discord.Color.blue()
  )
  
  await ctx.send(embed=embed)

@bot.command(name='mc', help='Gestiona las funciones del servidor de Minecraft')
async def minecraft(ctx: commands.Context, server: str=None):
  if server:
    await show_server(ctx, server)
  else:
    await list_servers(ctx)

async def list_servers(ctx: commands.Context):
  aternos = Client.from_credentials(
    os.getenv('USERNAME'), os.getenv('PASSWORD'))
  servers = aternos.list_servers()
    
  embeds: list = []
    
  for server in servers:
    embed = discord.Embed(
      color=discord.Color.dark_orange())
    embed.add_field(
      name='Nombre', value=f'`{server.subdomain}`', inline=True)
    embed.add_field(name='Software',
      value=f'`{server.software}`', inline=True)
    embed.add_field(
      name='Versión', value=f'`{server.version}`', inline=True)
    
    status = server.status.split(' ')[-1]
    
    match status:
      case 'online':
        circle = ':green_circle:'
      case 'offline':
        circle = ':red_circle:'
      case 'starting':
        circle = ':yellow_circle:'
      case 'loading':
        circle = ':orange_circle:'
      
    embed.add_field(
      name='Estado', value=f'{circle} `{status.capitalize()}`', inline=True)
    embeds.append(embed)
    
  await ctx.send(embeds=embeds)

async def show_server(ctx: commands.Context, server_name: str):
  aternos: Client = Client.from_credentials(os.environ['USERNAME'], os.environ['PASSWORD'])
  servers = aternos.list_servers()

  for server in servers:
    if (server_name.lower() in server.subdomain.lower()):
      embed = discord.Embed(
        title=f'{ctx.guild.name}', 
        description='Información del servidor de Minecraft.', 
        color=discord.Color.green()
      )
  
      start: Button = Button(style=discord.ButtonStyle.green, label='Iniciar', custom_id='start')
      
      view: View = View()
      view.add_item(start)    

      embed.set_thumbnail(url='https://img.icons8.com/doodle/452/minecraft-logo.png')
      embed.add_field(name='Dirección', value=f'`{server.address}`', inline=True)
      embed.add_field(name='Software', value=f'`{server.software}`', inline=True)
      embed.add_field(name='Versión', value=f'`{server.version}`', inline=True)

      if (server.status == 'online'):
        players = ''
        for player in server.players_list:
          players += f'- {player}\n'
        embed.add_field(name='Jugadores', value=f'`{players}`', inline=True)
      
      if (server.status != 'offline'):
        start.label = server.status.capitalize()
        start.disabled = True
        start.style = discord.ButtonStyle.gray
        
      async def on_start(interaction: discord.Interaction):
        start.disabled = True
        
        server.start()
  
        start.label = 'Loading'
        await interaction.response.edit_message(embed=embed, view=view)
        await interaction.channel.send(f'Iniciando el servidor {server.subdomain}...')
      
      start.callback = on_start

      await ctx.send(embed=embed, view=view)
      
      return

  await ctx.send(f'No se ha encontrado el servidor \'{server_name}\'.')

bot.run(os.environ['TOKEN'])
