import discord
from discord.ext import commands
from functions import *
from datetime import datetime

docs = {

    "aliases":[],

    "usage":"!test",

    "description":"owo? What's this?",

    "category":"fluff"
    
    }

def setup(client):
    @client.command()
    @commands.cooldown(1,15,commands.BucketType.user)
    async def test(ctx):     
        await ctx.send("owo", delete_after=60)