import discord
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

INSTANCE_ID = os.getenv("INSTANCE_ID")
TOKEN = os.getenv('TOKEN')

Intents = discord.Intents.all()
client = discord.Client(intents = Intents)

ec2 = boto3.resource('ec2')
instance = ec2.Instance(INSTANCE_ID)

@client.event
async def on_ready():
    print("ログインしました")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '/start':
        print("Instance is starting")
        await message.channel.send('Instance is starting')
        instance.start()
        instance.wait_until_running()
        print("Instance started")
        await message.channel.send('Instance is running')
        ip = instance.public_ip_address
        print(f"IP_ADDRESS: {ip}")

    if message.content == '/stop':
        print("instance is stopping")
        await message.channel.send('instance is stopping')
        instance.stop()
        instance.wait_until_stopped()
        print("instance is stopped")
        await message.channel.send('instance is stopped')

client.run(TOKEN)