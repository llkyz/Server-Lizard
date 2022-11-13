import discord
from discord.ext import commands
import random
from functions import *


def setup(client):
    @client.command() # Give another user some coins
    async def give(ctx):
        userData = await checkAccount(ctx)
        if userData != None:
            msgData = ctx.message.content.split(" ")
            if len(msgData) != 3:
                await ctx.send('Invalid syntax! Please use `!give [@user] [amount]`')
            else:
                try:
                    receiverId = int(msgData[1].replace('<@','').replace('>',''))
                    guild = await client.fetch_guild(ctx.guild.id)
                    getUser = await guild.fetch_member(receiverId)
                    giveAmount = int(msgData[2])
                except:
                    await ctx.send('Invalid syntax! Please use `!give [@user} [amount]`')
                else:
                    if getUser is None:
                        await ctx.send('Invalid user! Please use `!give [@user] [amount]`')
                    elif giveAmount > userData["money"]:
                        await ctx.send('You don\'t have that many coins!')
                    else:
                        sqlCursor.execute('SELECT * FROM userDB WHERE userId = %s', (receiverId,))
                        receiverData = sqlCursor.fetchone()
                        if receiverData == None:
                            sql = "INSERT INTO userDB (userId, coins, daily) VALUES (%s, %s, %s)"
                            val = (receiverId, giveAmount, "0")
                            sqlCursor.execute(sql, val)
                        else:
                            sql = 'UPDATE userDB SET coins = %s WHERE userId = %s'
                            val = (receiverData[1]+giveAmount, receiverId)
                            sqlCursor.execute(sql, val)

                        sql = 'UPDATE userDB SET coins = %s WHERE userId = %s'
                        val = (userData["money"]-giveAmount, userData["id"])
                        sqlCursor.execute(sql, val)
                        sqlDb.commit()

                        await ctx.send(f'**🪙 {ctx.author.display_name}** gave **{"{:,}".format(giveAmount)}** coins to **{getUser.display_name}**!')