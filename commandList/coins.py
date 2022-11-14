import discord
from discord.ext import commands
from functions import *

docs = {

    "aliases":['coins', 'money', 'currency'],

    "usage":"!coins",

    "description":"Checks your coin balance. Spend them on a wide range of goodies and games! Get free coins every day with `!daily`.",

    "category":"economy"

    }

def setup(client):
    @client.command(aliases=['money','currency', 'coins']) # Checks your coin balance
    async def coin(ctx):
        userData = await checkAccount(ctx)
        if userData != None:
            await ctx.send(f'**{ctx.author.display_name} 🪙 |** You have **{"{:,}".format(userData["money"])}** coins')