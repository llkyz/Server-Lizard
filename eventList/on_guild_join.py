import discord
from discord.ext import commands

def setup(client):
    @client.event
    async def on_guild_join(guild):
        channel = guild.system_channel #getting system channel
        if channel.permissions_for(guild.me).send_messages: #making sure you have permissions
            await channel.send("Server Lizard 🦎 is here! Please use `!commands` to see a list of my commands.")
