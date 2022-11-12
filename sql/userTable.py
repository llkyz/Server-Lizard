import discord
from discord.ext import commands
from functions import *

def setup(client):
    @client.command()
    async def makeUserTable(ctx):
        if checkOwner(ctx):
            try:
                sqlCursor.execute("CREATE TABLE userDB (userId BIGINT, \
            coins INT(255), \
            daily VARCHAR(10)) \
            ")
                await ctx.reply("userDB created")
            except:
                await ctx.reply("userDB already exists")

    @client.command()
    async def emptyUserTable(ctx):
        if checkOwner(ctx):
            sqlCursor.execute('DELETE FROM userDB')
            sqlDb.commit()
            await ctx.reply("UserDB emptied")