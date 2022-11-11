import discord
from discord.ext import commands
import random

def setup(client):
    @client.command() #!roll
    async def roll(ctx):
        try:
            number = int(ctx.message.content.replace('!roll ',''))
            if number > 0:
                result = random.randint(1,number)
                await ctx.reply(f'🎲 Rolled {result}! 🎲')
            else:
                await ctx.reply(f'Please enter a valid number!')
        except:
            await ctx.reply('Please enter a positive number after !roll.')
