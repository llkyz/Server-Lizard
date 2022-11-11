# bot.py
import os
import discord
from discord.ext import commands
from discord import Button, ButtonStyle
from dotenv import load_dotenv
import random
import asyncio
import requests
import json
from datetime import datetime, timedelta
import time
import math

#### Bot Settings
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

#### Global Functions
def timeConvert(originalTime): #converts UTC to GMT+8
    newTime = originalTime + timedelta(hours=8)
    return newTime

#usage example: checkRoles(ctx.author, [1030144135560167464, 1035245311553196112])
#returns True if any of the roles in the array matches, else return False
def checkRoles(member, arr):
    for x in member.roles:
        for y in arr:
            if x.id == y:
                return True
    return False

#### Administrative
client.load_extension("commandList.admin")
client.load_extension("commandList.commands")
client.load_extension("commandList.populate")
client.load_extension("commandList.infraction")
client.load_extension("commandList.bulkdelete")
client.load_extension("commandList.selfdelete")
client.load_extension("commandList.timed")

#### Fluff
client.load_extension("commandList.test")
client.load_extension("commandList.greet")
client.load_extension("commandList.change")
client.load_extension("commandList.blahaj")

#### Games
client.load_extension("commandList.game")
client.load_extension("commandList.battle")
client.load_extension("commandList.roll")

#### User/Message Commands
client.load_extension("commandList.userCommandList.userProfile")
client.load_extension("commandList.messageCommandList.report")

#### Event Listeners
client.load_extension("eventList.on_ready")
client.load_extension("eventList.on_member_join")
client.load_extension("eventList.on_member_update")
client.load_extension("eventList.on_raw_reaction_add")
client.load_extension("eventList.on_message")

client.run(TOKEN)
