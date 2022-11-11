import discord
from discord.ext import commands

def setup(client):
    @client.command() #!test
    async def test(ctx):
        await ctx.send("owo")
