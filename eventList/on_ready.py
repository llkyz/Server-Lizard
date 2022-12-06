from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord
from discord.ext import commands
import asyncio
from functions import *

def setup(client):
    @client.event
    async def on_ready():
        async def checkFunc():
            await timedCheck(client)

        print("Timed checker initialized")
        scheduler = AsyncIOScheduler()
        scheduler.add_job(checkFunc, 'interval', minutes=1)
        scheduler.start()

        print(f'{client.user} is connected to the following guilds:\n')
        for guild in client.guilds:
            print(f'{guild.name} (id: {guild.id})')

        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name="!commands"))