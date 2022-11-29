import discord
from discord.ext import commands
from functions import *

def setup(client):
    @client.command(aliases=['setcoins'])
    async def setCoins(ctx):
        if checkOwner(ctx):
            msgData = ctx.message.content.split(" ")
            if len(msgData) != 3:
                await ctx.reply("Invalid arguments. Please use !setCoins [@user] [x]", delete_after=20)
            else:
                try:
                    userId = msgData[1].replace("<@", "").replace(">", "")
                    query = int(msgData[2])
                except:
                    await ctx.reply("Invalid arguments. Please use !setCoins [@user] [x]", delete_after=20)
                else:
                    sql = 'UPDATE userDB SET coins = %s WHERE userId = %s'
                    val = (query, userId)
                    sqlCursor.execute(sql, val)
                    sqlDb.commit()

                    await ctx.reply(f'Coins set to {"{:,}".format(query)}')
        else:
            embed = discord.Embed()
            embed.set_image(url='https://cdnmetv.metv.com/z50xp-1619719725-16226-list_items-no.jpg')
            await ctx.send(embed=embed, delete_after=20)

    @client.command(aliases=['setactivity'])
    async def setActivity(ctx):
        if checkOwner(ctx):
            msgData = ctx.message.content.split(" ")
            if len(msgData) != 2:
                await ctx.reply("Invalid arguments. Please use !setActivity [x]", delete_after=20)
            else:
                activity = discord.Game(name=f'{msgData[1]}')
                await client.change_presence(status=discord.Status.online, activity=activity)