import discord
from discord.ext import commands
import json
from functions import *

def setup(client):
    @client.event
    async def on_command_error(ctx,error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.reply('You\'re already using this command! Please complete it, or try again later', delete_after=10)