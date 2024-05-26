# Authors: Itzdan0ul & Parrot14 (2022)
# index.py

import os
from datetime import date 
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()

TOKEN: str = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.emojis = True
intents.dm_messages = True

bot = commands.Bot(command_prefix='->', intents=intents, help_command=None)

@bot.event
async def on_ready():
  thoughts: list = [
    'qué mamada hacer.', 
    'este pinche mundo muerto.',
    'que Dios nos ha abandonado.',
    'que soy muy miserable.',
    'que soy un fracaso.',
    'que soy un inútil.',
    'que la extraño mucho.',
  ]
  
  check_birthdays.start()
  
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{random.choice(thoughts)}'))

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
  if isinstance(error, commands.CommandNotFound):
    messages: list = [
      '*¡Ese comando no existe, cabrón!*', 
      '*¡No parece que hayas leído la documentación!*',
      '*¿Qué haces todavía aquí, payaso...? Tecleando comandos incorrectos.* <:yawning_face:1054985333160292404>',
      '*¡Qué desastre has causado con ese comando equivocado! Ahora tendré que quitarme la vida...*',
      '*¡Debiste haber leído las instrucciones antes de ejecutar el comando!*',
      '*¡Qué estupidez has cometido!*',
      '*¡No me digas que te equivocaste de nuevo! ¡Eres una cabeza hueca!*'
    ]
    await ctx.send(random.choice(messages))
  else:
    raise error

@bot.command(name='help')
async def help(ctx: commands.Context):
  embed = discord.Embed(
    title='Comandos', 
    description='''
    Lista de comandos disponibles.
    
    **El prefijo es `->`.*

    *help* - Muestra la lista de comandos disponibles.
    *url_snippet* - `CHANNEL PAGE_NAME [DESCRIPTION [LINK [IMAGES [NOTES]]]]` - Envía un widget de contenido a un canal específicado.
    *code_snippet* - `CHANNEL [TITLE [CODE [LANGUAGE]]]` - Envía un snippet de código a un canal específicado.
    *docs_snippet* - `CHANNEL [TITLE [TEXT]]` - Envía un snippet de documentación a un canal específicado.
    ''', 
    color=discord.Color.blue()
  )
  
  await ctx.send(embed=embed)

@bot.command(name='url_snippet')
async def url_snippet(ctx: commands.Context, 
                 channel: discord.TextChannel, 
                 title: str, 
                 desc: str=None, 
                 link: str=None, 
                 image: str=None,
                 notes: str=None):
  """
  This function creates a snippet for link organization.
  
  Parameters
  ----------
  `channel`: discord.TextChannel
      The text channel where the snippet will be sent (Send channel id).
    `title`: str
      The page title.
    `desc`: str
      The page description.
    `link`: str
      The page URL.
    `image`: str
      The page image URL.
    `notes`: str
      Additional notes.
  
  Returns
  -------
  T
    The page snippet.
  """

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
        title=f'{title}',
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

@bot.command(name='code_snippet')
async def code_snippet(ctx: commands.Context, 
                channel: discord.TextChannel, 
                title: str=None, code: str=None,
                lang: str=None):
  """
  This function creates a snippet for code organization.

  Parameters
  ----------
  `channel`: discord.TextChannel
      The text channel where the snippet will be sent (Send channel id).
    `title`: str
      The code title.
    `code`: str
      The code.
    `lang`: str
      The code language.
      
  Returns
  -------
  T
    The code snippet.
  """
  
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
        title=f'{title}',
        description=f"""```{lang}{code}```""",
        color=colors[random.choice(list(colors))],
      )

      await channel.send(embed=embed)
      break

@bot.command(name='docs_snippet')
async def docs_snippet(ctx: commands.Context, channel: discord.TextChannel, title: str=None, text: str=None):
  """
  The function creates a snippet that is intended to be informative.
  
  Parameters
  ----------
  `channel`: discord.TextChannel
      The text channel where the snippet will be sent (Send channel id).
    `title`: str
      The  The title of the snippet.
    `text`: str
      The text of the snippet.
  
  Returns
  -------
  T
    The docs snippet.
  """

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
        title=f'{title}',
        description=f"""{text}""",
        color=colors[random.choice(list(colors))],
      )

      await channel.send(embed=embed)
      break

@tasks.loop(hours=24)
async def check_birthdays(): 
  birthdays: list = [
    (1, 10, 895480692522250271), # Daniel Romero
    (3, 2, 791473769075703848), # Ivan Huerta
    (3, 10, 434778407239286805), # Erik Villegas
    (5, 6, 430916352686030848), # Brayan Gay
    (6, 13, 430916352686030848), # Jose Ruiz
    (8, 8, 692240248368791573), # Luis Rayas
    (8, 9, 550544475420622849), # Alan Silva
    (9, 16, 751955612731965552), # Ale Silva
    (11, 18, 763491461118951426), # Dan Urtiz
    (12, 18, 405569777214685184) # Max Torres
  ]

  today: date = date.today()
  current_month: int = today.month
  current_day: int = today.day

  gifs: list = [
      'https://media1.tenor.com/m/SVfm3-297cIAAAAd/konosuba-aqua-cum.gif',
      'https://media1.tenor.com/m/toaos0JEj1gAAAAd/cum-cake.gif',
      'https://media.tenor.com/bh9MAiCpL6wAAAAj/birthday-cake.gif'
    ]

  for month, day, user_id in birthdays:
    if current_month == month and current_day == day:
      embed = discord.Embed(
        title='¡Feliz CUMpleaños! 🎉🎉🎉',
        description=f"""
          Para ti cumpleaños feliz, <@{user_id}>

          hora un poema para ti:
          En tu cumpleaños, mezcla de gloria y aflicción,
          Un año más se suma, con su carga de frustración.
          Las arrugas avanzan, la juventud se va,
          Pero la sabiduría y las memorias, ¡esas siempre quedarán!

          Desesperanza y brillo, en un solo día,
          Ríe y llora, en esta travesía.
          Porque aunque el tiempo pase y se sienta cruel,
          Las vivencias y risas son el mejor laurel.

          Feliz cumpleaños, en esta dualidad,
          Donde el pesar se mezcla con la felicidad.
          Brindemos por lo bueno y lo malo también,
          Porque vivir significa abrazar lo que viene.
          """,
          color=discord.Color.purple()
        )
      
      embed.set_image(url=random.choice(gifs))

      channel = bot.get_channel(1244398461093285929)
      
      await channel.send(embed=embed)
      break

@check_birthdays.before_loop
async def before_check_birthdays():
  await bot.wait_until_ready()

bot.run(os.environ['TOKEN'])
