# Author: Itzdan0ul & Parrot14 (2022)
# index.py

import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
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
    `widget  CHANNEL PAGE_NAME [DESCRIPTION [LINK [IMAGES [NOTES]]]]` - Envía un widget de contenido a un canal específicado.
    ''', 
    color=discord.Color.blue()
  )
  
  await ctx.send(embed=embed)

@bot.command(name='widget')
async def widget(ctx: commands.Context, 
                 channel: discord.TextChannel, 
                 page: str, 
                 desc: str=None, 
                 link: str=None, 
                 image: str=None,
                 notes: str=None):
  for role in ctx.author.roles:
    if role.name == 'Programmer':
      colors = {
        'red': discord.Color.red(),
        'green': discord.Color.green(),
        'blue': discord.Color.blue(),
        'yellow': discord.Color.gold(),
        'purple': discord.Color.purple(),
        'orange': discord.Color.orange(),
      }
      embed = discord.Embed(
        title=f'{page}',
        description=f'{desc}',
        color=colors[random.choice(list(colors))],
      )
      
      embed.add_field(name='URL', value=f'https://{link}', inline=False)

      if image:
          embed.set_thumbnail(url=f'{image}')
      
      if notes:
        embed.add_field(name='Notas', value=f'{notes}', inline=False)

      await channel.send(embed=embed)
      break

bot.run(os.environ['TOKEN'])
