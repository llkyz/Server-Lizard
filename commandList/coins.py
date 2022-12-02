import discord
from discord.ext import commands
from functions import *

docs = {

    "aliases":['coins', 'money', 'currency', 'balance', 'wallet'],

    "usage":"!coins",

    "description":"Checks your coin balance. Spend them on a wide range of goodies and games! Get free coins every day with `!daily`.",

    "category":"economy"

    }

def setup(client):
    @client.command(aliases=['money','currency', 'coins', 'balance', 'wallet']) # Checks your coin balance
    @commands.cooldown(1,15,commands.BucketType.user)
    async def coin(ctx):
        userData = await fetchUserData(ctx.author)
        if userData != None:
            await ctx.send(f'**<:lizard_coin:1047527590677712896> | {ctx.author.display_name}** You have **{"{:,}".format(userData["coins"])}** coins')