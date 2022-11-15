import discord
from discord.ext import commands
from functions import *

def setup(client):
    @client.command(aliases=['makeusertable'])
    async def makeUserTable(ctx):
        if checkOwner(ctx):
            try:
                sqlCursor.execute("CREATE TABLE userDB (userId BIGINT, \
            coins INT(255), \
            daily VARCHAR(10)) \
            ")
                await ctx.reply("userDB created")
            except Exception as e:
                await ctx.reply(e)

    @client.command(aliases=['emptyusertable','clearUserTable', 'clearusertable'])
    async def emptyUserTable(ctx):
        if checkOwner(ctx):
            sqlCursor.execute('DELETE FROM userDB')
            sqlDb.commit()
            await ctx.reply("UserDB emptied")