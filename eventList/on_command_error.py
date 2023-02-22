import discord
from discord.ext import commands
import json
from functions import *
from datetime import datetime

def setup(client):
    @client.event
    async def on_command_error(ctx,error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.reply('You\'re already using this command! Please complete it, or try again later.', delete_after=10)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Please try again <t:{(int(error.retry_after) + int(datetime.timestamp(datetime.now())))}:R>.', delete_after=20)
        else:
            print(error)