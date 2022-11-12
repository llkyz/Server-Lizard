import discord
from discord.ext import commands

def setup(client):
    client.remove_command('help')
    @client.command(aliases=['command','help']) #!commands            
    async def commands(ctx):
        embed=discord.Embed(title=f'Lizard Commands!', description='Use !help or !commands to show this list.\nTo use a command, enter: `!{command}`',color=0x14AB49)
        embed.add_field(name='🙃 **Fluff**', value='`test` `greet` `change` `blahaj`', inline=False)
        embed.add_field(name='🪙 **Economy**', value='`coins` `daily` `give`', inline=False)
        embed.add_field(name='🎮 **Games**', value='`roll` `battle`', inline=False)
        embed.add_field(name='🎲 **Gamble**', value='`rps` `blackjack`', inline=False)
        embed.add_field(name='📰 **Message Management**', value='`timed` `selfdelete`', inline=False)
        embed.add_field(name='👓 **Mod/Admin Use**', value='`admin`', inline=False)
        embed.add_field(name='**Additional Features**', value='Starboard / Post Reporting / Mod Pings', inline=False)
        await ctx.reply(embed=embed)