import discord
import os
import random
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive


load_dotenv('settings.env')
TOKEN = os.getenv('DISCORD_TOKEN')

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
async def ping(ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    await ctx.send(quote)

@bot.command(name="serverinfo", help="Muestra informacion sobre el servidor")
async def serverinfo(ctx):
    cantroles = cantchannels = cantemojis = 0
    owner = "No funciona"
    for channel in ctx.guild.channels:
        cantchannels+=1
    for rol in ctx.guild.roles:
        cantroles+=1
    for emoji in ctx.guild.emojis:
        cantemojis+=1
    for member in ctx.guild.members:
        if member.id == ctx.guild.owner_id:
            owner = member.display_name
    embed=discord.Embed(title="Informacion del Servidor", color=0x00bfff)
    embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
    embed.add_field(name="Nombre", value=f"{ctx.guild.name}", inline=True)
    embed.add_field(name="Miembros", value=f"{ctx.guild.member_count}", inline=True)
    embed.add_field(name="Dueño", value=f"{owner}", inline=False)
    embed.add_field(name="Canales", value=f"{cantchannels}", inline=True)
    embed.add_field(name="Roles", value=f"{cantroles}", inline=True)
    embed.add_field(name="Emojis", value=f"{cantemojis}", inline=True)
    await ctx.send(embed=embed)

@bot.command(name="roll", help="Tira un dado.")
async def roll(ctx, amax, atimes):
    times = int(atimes)
    max = int(amax)
    dice = []*times
    for i in range(times):
        dice.append(str(random.choice(range(1,max + 1))))
    await ctx.send(dice)

@bot.command(name="absolut", help="Devuelve el valor absoluto de un valor")
async def absolut(ctx, valor):
    valor = int(valor)
    if(valor < 0):
        valor = valor * -1
    await ctx.send(valor)

@bot.command(name="color", help="Permite a los nitro booster cambiar su color!")
async def color(ctx, ccolor):
    author = ctx.message.author
    guild = ctx.guild
    if author.premium_since != None:
        try:
            for rol in guild.roles:
                if rol.name == author.name:
                    colorrol = rol
                    flag = 1
            if flag == 0:
                await guild.create_role(name=author.name, colour=colors.get(ccolor))
                for rol in guild.roles:
                    if rol.name == author.name:
                        colorrol = rol
            await ctx.author.add_roles(colorrol)
            await ctx.send("Color cambiado con exito")
        except Forbidden:
            await ctx.send("**Error**: No tienes permiso ejecutar este comando")
        except HTTPException:
            await ctx.send("**Error**: Ocurrio un error al crear el rol :thinking:")
        except InvalidArgument:
            await ctx.send("**Error**: uso correcto `!color {colour}`/n" + colors)
    else:
        await ctx.send("Solo los nitro booster pueden cambiar su color")

keep_alive()
bot.run(TOKEN)
