import discord
from discord.ext import commands
from functions import *
import json
import asyncio
from discord import Button, ButtonStyle

docs = {

    "aliases":[],

    "usage":"!masskick [list of user IDs]",

    "description":"Nuke",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command()
    @commands.has_permissions(administrator = True)
    async def masskick(ctx):
        if not hasAdminRole(ctx) and checkOwner(ctx):
            await ctx.reply("You do not have permission to use this command!", delete_after=20)
            return
        
        kickList = ctx.message.content
        kickList = kickList.replace("!masskick", "")
        kickList = kickList.split()

        view = discord.ui.View()
        button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
        button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
        view.add_item(button1)
        view.add_item(button2)

        msg1 = await ctx.send(embed=discord.Embed(title=f'**Mass kick {len(kickList)} members?**'), view=view)

        def checkButton(m):
            return m.message == msg1 and m.user == ctx.author
        try:
            interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
        except asyncio.TimeoutError:
            await msg1.edit(content='Timed out!', view=None)
        else:
            await interacted.response.defer()
            await msg1.edit(view=None)
            
            if interacted.data['custom_id'] == 'cancel':
                return
            elif interacted.data['custom_id'] == 'confirm':
                for x in kickList:
                    try:
                        member = await ctx.guild.fetch_member(x)
                        await ctx.send(f"Kicking {member.mention} ({x})")
                        await member.kick()
                    except:
                        await ctx.send(f"Could not kick member ID {x}")
                await ctx.send(f'Mass kick complete')