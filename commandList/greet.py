import discord
from discord.ext import commands
import asyncio

def setup(client):
    @client.command() #!greet
    async def greet(ctx):
        channel = ctx.channel
        mymsg = await ctx.reply('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        try:
            msg = await client.wait_for('message', timeout=20, check=check)
        except asyncio.TimeoutError:
            await mymsg.edit(content='Timed out!')
        else:
            await msg.reply(f'Hello {msg.author.display_name}!')
