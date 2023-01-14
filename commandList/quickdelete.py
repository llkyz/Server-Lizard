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
                try:
                    if arg and int(arg) > 0:
                        if int(arg) == 1:
                            plural = "message"
                        else:
                            plural = "messages"
                        try:
                            deleted = await ctx.channel.purge(limit=int(arg))
                            embed=discord.Embed(title=f'{len(deleted)} {plural} deleted.', color=0x00FF00)
                            await ctx.send(embed=embed, delete_after=30)
                        except:
                            await ctx.send("Please use the following format: `!quickdelete [number]`", delete_after=20)
                    else:
                        await ctx.send("Please use the following format: `!quickdelete [number]`", delete_after=20)
                except Exception as e:
                    print(e)
                    await ctx.send("Please use the following format: `!quickdelete [number]`", delete_after=20)