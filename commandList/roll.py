import discord
from discord.ext import commands
import random

docs = {

    "aliases":['dice'],

    "usage":"!roll [number]",

    "description":"Rolls a random number between 0 and your chosen number.",

    "category":"games"
    
    }

def setup(client):
    @client.command(aliases=['dice']) #!roll
    async def roll(ctx):
        try:
            number = int(ctx.message.content.replace('!roll ',''))
            if number > 0:
                result = random.randint(1,number)
                await ctx.reply(f'🎲 Rolled {result}! 🎲')
            else:
                await ctx.reply(f'Please use the following format: !roll [number]', delete_after=20)
        except:
            await ctx.reply('Please use the following format: !roll [number]', delete_after=20)
