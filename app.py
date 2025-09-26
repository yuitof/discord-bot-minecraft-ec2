import discord
import os
import boto3

if os.environ.get('ENV') != 'production':
    from dotenv import load_dotenv
    load_dotenv()

Intents = discord.Intents.all()
client = discord.Client(intents = Intents)

ec2 = boto3.resource('ec2', region_name="ap-northeast-1")
instance = ec2.Instance(os.environ.get("INSTANCE_ID"))

@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.content == '/start':
        try:
            print('Starting instance...')
            await message.channel.send('Starting instance...')
            instance.start()
            instance.wait_until_running()
            print('Instance is running')
            await message.channel.send('Instance is running')
            await message.channel.send(f"IP_ADDRESS: {instance.public_ip_address}")
        except Exception as e:
            print('Failed to start instance', e)
            await message.channel.send('Failed to start instance😩')
            


    if message.content == '/stop':
        if instance.state['Name'] == 'running':
            try:
                print('Stopping instance...')
                await message.channel.send('Stopping instance...')
                instance.stop()
                instance.wait_until_stopped()
                print('Instance has been stopped')
                await message.channel.send('Instance has been stopped')
            except Exception as e:
                print('Failed to stop instance', e)
                await message.channel.send('Failed to stop instance😣')
        else:
            print('Instance isn\'t running')
            await  message.channel.send('Instance isn\'t running')

    if message.content == '/state':
        await message.channel.send('Running' if instance.state['Name'] == 'running' else 'Stopped')

client.run(os.environ.get('PUBLIC_KEY'))
