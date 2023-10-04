import discord
from discord.ext import commands
from discord import Button, ButtonStyle
from functions import *

docs = {

    "aliases":[''],

    "usage":"!backup [message link]",

    "description":"Copy a message from a separate location to the current channel.",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command()
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
    async def backup(ctx, arg=None,):
        if not hasAdminRole(ctx) and not checkOwner(ctx):
            await ctx.reply("You do not have permission to use this command!", delete_after=20)
            return

        if arg == None:
            await ctx.reply("Please enter a message link to backup", delete_after=20)
            return
        
        if "https://discord.com/channels/" not in arg:
            await ctx.reply("Please enter a valid message link", delete_after=20)
            return
        
        arg = arg.replace("https://discord.com/channels/", "")
        arg = arg.split("/")
        for x in arg:
            if not x.isnumeric():
                await ctx.reply("Invalid arguments", delete_after=20)
                return
            
        try:
            myChannel = client.get_channel(int(arg[1]))
            fetched = await myChannel.fetch_message(int(arg[2]))
        except:
            await ctx.author.send(embed=discord.Embed(title="Error, could not retrieve message. Please try again"))
            return
        
        embed = False
        if fetched.embeds:
            embed = fetched.embeds[0]

        attachments = False
        attachmentList = []
        if fetched.attachments:
            attachments = fetched.attachments
            for x in attachments:
                await x.save(x.filename)
                attachmentList.append(discord.File(x.filename, filename = x.filename))

        await ctx.message.delete()
        if embed:
            if attachments:
                await ctx.send(fetched.content, embed=embed, files=attachmentList)
            else:
                await ctx.send(fetched.content, embed=embed)
        else:
            if attachments:
                await ctx.send(fetched.content, files=attachmentList)
            else:
                await ctx.send(fetched.content)