import os
import json
from roll_functions import *
import discord

def get_keys(path):
    try:
        with open(path) as f:
            print(f"{path} has been opened")
            return json.load(f)
    except Exception as e:
        print(e)
        return None

keys = get_keys('api_key.json')

TOKEN = keys['bot_token'] #''NzMzMzYxNDkxNDYxNDA2ODU5.XxCCHA.C4H6u1m6KohrrsCa7Z-BFbKJNtw'
# GUILD = keys['guild_name'] #''aslidsiksoraksi'


client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0:3] == '~d ' or message.content[0:3] == '~r ' or message.content[0:5] == '~roll':
        if message.content[0:3] == '~d ' or message.content[0:3] == '~r ':
            their_roll = message.content[3:].lower()
        if message.content[0:5] == '~roll':
            their_roll = message.content[5:].lower()
        try:
            roll_list = roll_them_dice(their_roll)
                
            for roll in roll_list:
                try:
                    roll_message = str(roll['message'])
                    response = f'{message.author.mention} {roll_message}'
                    await message.channel.send(response)
                except: 
                    pass
        except:
            await message.channel.send(f'{message.author.mention} - sorry, your input was not recognized')

    
        

client.run(TOKEN)