import os
import vars
import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return



    if message.content == "doge! gaybar":
        await message.channel.send(random.choice(vars.lyrics))
    if message.content == "doge! eggbar":
        await message.channel.send(random.choice(vars.lyricsegg))
    if message.content == "doge! sad":
        await message.channel.send(random.choice(vars.saddoge))


client.run(TOKEN)