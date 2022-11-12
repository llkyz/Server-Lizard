import discord
from discord.ext import commands
from functions import *


def setup(client):
    @client.command(aliases=['money','currency', 'coins']) # Get a random number of coins every day
    async def coin(ctx):
        userData = await checkAccount(ctx)
        if userData != None:
            await ctx.reply(f'**{ctx.author.display_name} 🪙 |** You have **{"{:,}".format(userData["money"])}** coins')