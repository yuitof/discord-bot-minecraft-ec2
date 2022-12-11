import discord
import os
import boto3
from dotenv import load_dotenv

load_dotenv()

INSTANCE_ID = os.getenv("INSTANCE_ID")
TOKEN = os.getenv('TOKEN')


Intents = discord.Intents.all()
client = discord.Client(intents = Intents)

ec2 = boto3.resource('ec2', region_name="ap-northeast-1")
instance = ec2.Instance(INSTANCE_ID)

@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '/start':
        print("Instance is being started")
        await message.channel.send('Instance is being started')
        instance.start()
        instance.wait_until_running()
        print("Instance is running")
        await message.channel.send('Instance is running')
        ip = instance.public_ip_address
        print(f"IP_ADDRESS: {ip}")
        await message.channel.send(f"IP_ADDRESS: {ip}")

    if message.content == '/stop':
        print("Instance is being stopped")
        await message.channel.send('Instance is being stopped')
        instance.stop()
        instance.wait_until_stopped()
        print("Instance has been stopped")
        await message.channel.send('Instance has been stopped')

    if message.content == '/state':
        if instance.state['Name'] == 'running':
            print('Instance is running')
            await message.channel.send('Instance is running')
        else:
            print('Instance has been stopped')
            await message.channel.send('Instance has been stopped')

client.run(TOKEN)
