import discord
from discord.ext import commands
import asyncio

def setup(client):
    @client.event
    async def on_ready():
        print(f'{client.user} is connected to the following guilds:\n')
        for guild in client.guilds:
            print(
                f'{guild.name}(id: {guild.id})\n'
            )

        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name="!commands"))