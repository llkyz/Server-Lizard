import discord
from discord.ext import commands
from functions import *

def setup(client):
    @client.command() #!admin
    async def admin(ctx):
        if checkRoles(ctx.author, [423458739656458243, 407557898638589974]):
            await ctx.message.delete()
            embed=discord.Embed(title=f'Admin commands for Server Lizard', description='To use a command, enter: `!{command}`',color=0x14AB49)
            embed.add_field(name='📰 **Message Management**', value='`bulkdelete`', inline=False)
            embed.add_field(name='👓 **Administrative**', value='~~`roles`~~', inline=False)
            embed.add_field(name='❌ **Disciplinary**', value='`infraction add` `infraction remove`', inline=False)
            await ctx.author.send(embed=embed)
