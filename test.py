import discord
import os
from dotenv import load_dotenv

load_dotenv()

Intents = discord.Intents.all()
client = discord.Client(intents = Intents)

TOKEN = os.getenv('TOKEN')
print(TOKEN)

@client.event
async def on_ready():
    print("ログインしました")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '/neko':
        await message.channel.send('にゃーん')

client.run(TOKEN)