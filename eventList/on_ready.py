import discord
from discord.ext import commands

def setup(client):
    @client.event
    async def on_ready():
        print(f'{client.user} is connected to the following guilds:\n')
        for guild in client.guilds:
            print(
                f'{guild.name}(id: {guild.id})\n'
            )
