import discord
import os
import random
import requests
import json
from discord.ext import commands
from keep_alive import keep_alive
from replit import db

TOKEN = os.environ['DISCORD_TOKEN']

intents = discord.Intents().all()

bot = commands.Bot(command_prefix='!', intents=intents)

colors = {
    "red": 0xff0000,
    "blue": 0x0000ff,
    "green": 0x00ff00,
}


@bot.event
async def on_ready():
    print(f"{bot.user} esta online! Lista de servidores:")
    for guild in bot.guilds:
        print(f"{guild.name}(id: {guild.id})")


@bot.command(name="ping", help="Pong!")
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command(name="quote", help="Quote random de ZenQuotes")
async def quote(ctx):
  try:
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    await ctx.send(quote)
  except:
    await ctx.send("**Error Inesperado**")


@bot.command(name="serverinfo", help="Muestra informacion sobre el servidor")
async def serverinfo(ctx):
  try:
    cantroles = cantchannels = cantemojis = 0
    owner = "No funciona"
    for channel in ctx.guild.channels:
        cantchannels += 1
    for rol in ctx.guild.roles:
        cantroles += 1
    for emoji in ctx.guild.emojis:
        cantemojis += 1
    for member in ctx.guild.members:
        if member.id == ctx.guild.owner_id:
            owner = member.display_name
    embed = discord.Embed(title="Informacion del Servidor", color=0x00bfff)
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    embed.add_field(name="Nombre", value=f"{ctx.guild.name}", inline=True)
    embed.add_field(name="Miembros",
                    value=f"{ctx.guild.member_count}",
                    inline=True)
    embed.add_field(name="Dueño", value=f"{owner}", inline=False)
    embed.add_field(name="Canales", value=f"{cantchannels}", inline=True)
    embed.add_field(name="Roles", value=f"{cantroles}", inline=True)
    embed.add_field(name="Emojis", value=f"{cantemojis}", inline=True)
    await ctx.send(embed=embed)
  except:
    await ctx.send("**Error inesperado**")


@bot.command(name="roll", help="Tira un dado.")
async def roll(ctx, amax, atimes):
  try:
    times = int(atimes)
    max = int(amax)
    dice = [] * times
    for i in range(times):
        dice.append(str(random.choice(range(1, max + 1))))
    await ctx.send(dice)
  except:
    await ctx.send("**Error**: `!roll [caras] [dados]`")


@bot.command(name="absolut", help="Devuelve el valor absoluto de un valor")
async def absolut(ctx, valor):
  try:
    valor = int(valor)
    if (valor < 0):
        valor = valor * -1
    await ctx.send(valor)
  except:
    await ctx.send("**Error**: `!absolut [number]`")


@bot.command(name="color", help="Permite cambiar su color!")
async def color(ctx, ccolor):
    author = ctx.message.author
    guild = ctx.guild
    #if author.premium_since != None:
    try:
        for rol in guild.roles:
            if rol.name == author.name:
                colorrol = rol
                flag = 1
        if flag == 0:
            await guild.create_role(name=author.name)
            for rol in guild.roles:
                if rol.name == author.name:
                    colorrol = rol
        await colorrol.edit(colour=colors.get(ccolor))
        await author.add_roles(colorrol)
        await ctx.send("Color cambiado con exito")
    except:
        await ctx.send("**Error Inesperado**")
    #else:
    #   await ctx.send("Solo los nitro booster pueden cambiar su color")


keep_alive()
bot.run(TOKEN)
