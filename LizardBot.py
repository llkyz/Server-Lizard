import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import glob
import asyncio

# from discord import Button, ButtonStyle
# import random
# import requests
# import json
# from datetime import datetime, timedelta
# import time
# import math

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

myfolders = ["commandList/*.py", "commandList/messageCommandList/*.py", "commandList/userCommandList/*.py", "eventList/*.py", "sql/*.py"]
for folderPath in myfolders:
    for x in glob.glob(folderPath):
        client.load_extension(x.replace("\\", ".").replace("/", ".").replace(".py", ""))

client.run(TOKEN)