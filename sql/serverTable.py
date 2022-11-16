import discord
from discord.ext import commands
from functions import *

def setup(client):
    @client.command(aliases=['makeservertable'])
    async def makeServerTable(ctx):
        if checkOwner(ctx):
            try:
                sqlCursor.execute("CREATE TABLE serverDB (serverId BIGINT, \
            serverName VARCHAR(100), \
            adminRoles JSON, \
            embedRoles JSON, \
            adminPingChannel BIGINT, \
            userProfilesChannel BIGINT, \
            roleSaveChannel BIGINT, \
            reportChannel BIGINT, \
            starboardChannel JSON, \
            starboardSources JSON) \
            ")
                await ctx.reply("ServerDB created")
            except Exception as e:
                await ctx.reply(e)
    
    @client.command(aliases=['emptyservertable', 'clearservertable', 'clearServerTable'])
    async def emptyServerTable(ctx):
        if checkOwner(ctx):
            sqlCursor.execute('DELETE FROM serverDB')
            sqlDb.commit()
            await ctx.reply("ServerDB emptied")

    @client.command(aliases=['dropservertable'])
    async def dropServerTable(ctx):
        if checkOwner(ctx):
            sqlCursor.execute('DROP TABLE serverDB')
            sqlDb.commit()
            await ctx.reply("ServerDB yeeted and deleted")