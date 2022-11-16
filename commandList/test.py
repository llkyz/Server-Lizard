import discord
from discord.ext import commands
from functions import *

docs = {

    "aliases":[],

    "usage":"!test",

    "description":"owo? What's this?",

    "category":"fluff"
    
    }

def setup(client):
    @client.command() #!test
    async def test(ctx):
        await ctx.send("owo")