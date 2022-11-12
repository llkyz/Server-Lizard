import discord
from discord.ext import commands
from functions import *

def setup(client):
    @client.command()
    async def setCoins(ctx):
        if checkOwner(ctx):
            msgData = ctx.message.content.split(" ")
            if len(msgData) != 2:
                await ctx.reply("Invalid arguments. Please use !setCoins [x]")
            else:
                try:
                    query = int(msgData[1])
                except:
                    await ctx.reply("Invalid arguments. Please use !setCoins [x]")
                else:
                    sql = 'UPDATE userDB SET coins = %s WHERE userId = %s'
                    val = (query, ctx.author.id)
                    sqlCursor.execute(sql, val)
                    sqlDb.commit()

                    await ctx.reply(f'Coins set to {query}')