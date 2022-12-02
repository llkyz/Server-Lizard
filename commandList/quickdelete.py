import discord
import math
from functions import *

docs = {

    "aliases":[],

    "usage":"!quickdelete [number]",

    "description":"Deletes [numberr] of the most recent messages from any channel.\n\nCAUTION: Messages will be permanently deleted and cannot be retrieved.",

    "category":"admin-messages"
    
    }

def setup(client):
    @client.command()
    async def quickdelete(ctx, arg=None):
        try:
            await ctx.message.delete()
        except:
            await ctx.author.send(f'Please use this command in a server channel.')
            return
        else:
            if hasAdminRole(ctx) or checkOwner(ctx):
                if arg:
                    try:
                        deleted = await ctx.channel.purge(limit=int(arg))
                        embed=discord.Embed(title=f'{len(deleted)} messages deleted.', color=0x00FF00)
                        await ctx.send(embed=embed)
                    except:
                        await ctx.send("Please use the following format: !quickdelete [number]", delete_after=20)
                else:
                    await ctx.send("Please use the following format: !quickdelete [number]", delete_after=20)