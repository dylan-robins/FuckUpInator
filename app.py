import atexit
import logging
from datetime import datetime, timedelta
from os import environ

import discord
import humanize

from db import db

print("Creating discord client...")
client = discord.Client()

print("Creating database...")
db = db("database.dat")

@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

@client.event
async def on_message(message):
    print("Received message")
    if message.author == client.user:
        return

    if message.content.startswith('!check'):
        ids = (user.id for user in message.mentions)
        msg = []
        for id in ids:
            try:
                last_fu = db.get_user_fu(id)
                fu_delta = humanize.naturaltime(datetime.now() - last_fu)
                msg.append(f"<@{id}> last fucked up {fu_delta} ago.")

            except KeyError:
                msg.append(f"<@{id}> hasn't fucked up yet. Boring!")


        await message.channel.send("\n".join(msg))
    
    if message.content.startswith('!reset'):
        ids = (user.id for user in message.mentions)
        msg = []
        for id in ids:
            try:
                last_fu = db.get_user_fu(id)
                fu_delta = humanize.naturaltime(datetime.now() - last_fu)
                msg.append(f"Restarted clock. <@{id}> last fucked up {fu_delta}.")

            except KeyError:
                msg.append(f"Started clock. <@{id}> hadn't fucked up yet!")
            
            db.set_user_fu(id, datetime.now())


        await message.channel.send("\n".join(msg))

def exit_handler():
    db.save()

atexit.register(exit_handler)

client.run(environ['DISCORD_TOKEN'])
