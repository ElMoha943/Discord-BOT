import os
import random
import discord
from discord.ext import commands

TOKEN = {BOT-TOKEN}

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f"{bot.user} esta online! Lista de servidores:")
    for guild in bot.guilds:
        print(f"{guild.name}(id: {guild.id})")

@bot.command(name="serverinfo", help="Muestra informacion sobre el servidor")
async def serverinfo(ctx):
    cantroles = cantchannels = cantemojis = 0
    owner = "none"
    for channel in ctx.guild.channels:
        cantchannels+=1
    for rol in ctx.guild.roles:
        cantroles+=1
    for emoji in ctx.guild.emojis:
        cantemojis+=1
    for member in ctx.guild.members:
        if member.id == ctx.guild.owner_id:
            owner=member.display_name
            break;
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

bot.run(TOKEN)
