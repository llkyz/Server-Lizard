import discord
from discord.ext import commands
from functions import *

def setup(client):
    @client.command(aliases=['makeusertable'])
    async def makeUserTable(ctx):
        if checkOwner(ctx):
            try:
                sqlCursor.execute("CREATE TABLE userDB (userId BIGINT, \
            userName VARCHAR(50), \
            coins INT(255), \
            daily VARCHAR(10)) \
            ")
                await ctx.reply("UserDB created")
            except Exception as e:
                await ctx.reply(e)

    @client.command(aliases=['emptyusertable','clearUserTable', 'clearusertable'])
    async def emptyUserTable(ctx):
        if checkOwner(ctx):
            sqlCursor.execute('DELETE FROM userDB')
            sqlDb.commit()
            await ctx.reply("UserDB emptied")

    @client.command(aliases=['dropusertable'])
    async def dropUserTable(ctx):
        if checkOwner(ctx):
            sqlCursor.execute('DROP TABLE userDB')
            sqlDb.commit()
            await ctx.reply("UserDB yeeted and deleted")