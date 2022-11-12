import discord
from discord.ext import commands
from functions import *

def setup(client):
    @client.command()
    async def makeServerTable(ctx):
        if checkOwner(ctx):
            try:
                sqlCursor.execute("CREATE TABLE serverDB (serverId BIGINT, \
            adminRoles JSON, \
            adminPingEnabled INT(1), \
            adminPingChannel BIGINT, \
            userProfilesEnabled INT(1), \
            userProfilesChannel BIGINT, \
            reportChannelEnabled INT(1), \
            reportChannel BIGINT, \
            starboardEnabled INT(1), \
            starboardChannel BIGINT, \
            starboardSources JSON) \
            ")
                await ctx.reply("serverDB created")
            except:
                await ctx.reply("serverDB already exists")
    
    @client.command()
    async def emptyServerTable(ctx):
        if checkOwner(ctx):
            sqlCursor.execute('DELETE FROM serverDB')
            sqlDb.commit()
            await ctx.reply("ServerDB emptied")