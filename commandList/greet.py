import discord
from discord.ext import commands
import asyncio

docs = {

    "aliases":[],

    "usage":"!greet",

    "description":"Say hello to me!",

    "category":"fluff"
    
    }

def setup(client):
    @client.command()
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
    async def greet(ctx):
        channel = ctx.channel
        mymsg = await ctx.reply('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        try:
            msg = await client.wait_for('message', timeout=60, check=check)
        except asyncio.TimeoutError:
            await mymsg.edit(content='Timed out!')
        else:
            await msg.reply(f'Hello {msg.author.display_name}!')
