import discord
from discord.ext import commands
from functions import *

docs = {

    "aliases":[],

    "usage":"!give [@user] [amount]",

    "description":"Gives another user some of your coins. Spread the love!",

    "category":"economy"
    
    }

def setup(client):
    @client.command() # Give another user some coins
    async def give(ctx):
        userData = await fetchUserData(ctx.author)

        if userData != None:
            msgData = ctx.message.content.split(" ")
            if len(msgData) != 3:
                await ctx.send('Invalid syntax! Please use `!give [@user] [amount]`', delete_after=20)
            else:
                try:
                    receiverId = int(msgData[1].replace('<@','').replace('>',''))
                    guild = await client.fetch_guild(ctx.guild.id)
                    getUser = await guild.fetch_member(receiverId)
                    receiverData = await fetchUserData(getUser)
                    giveAmount = int(msgData[2])
                except:
                    await ctx.send('Invalid syntax! Please use `!give [@user] [amount]`', delete_after=20)
                else:
                    if receiverId == ctx.author.id:
                        await ctx.send('You can\'t give coins to yourself!', delete_after=20)
                    elif getUser is None:
                        await ctx.send('Invalid user! Please use `!give [@user] [amount]`', delete_after=20)
                    elif giveAmount < 1:
                        await ctx.send('You can\'t give negative coins! 😠', delete_after=20)
                    elif giveAmount > userData["coins"]:
                        await ctx.send('You don\'t have that many coins!', delete_after=20)
                    elif receiverData['coins'] + giveAmount > 2147483647:
                        await ctx.send(f'{getUser.display_name} cannot receive any more coins.')
                    else:
                        sqlCursor.execute('SELECT * FROM userDB WHERE userId = %s', (receiverId,))
                        receiverData = sqlCursor.fetchone()
                        if receiverData == None:
                            sql = "INSERT INTO userDB (userId, userName, coins, daily) VALUES (%s, %s, %s, %s)"
                            val = (receiverId, getUser.name + "#" + getUser.discriminator, giveAmount, "0")
                            sqlCursor.execute(sql, val)
                        else:
                            sql = 'UPDATE userDB SET coins = %s, userName = %s WHERE userId = %s'
                            val = (receiverData[2]+giveAmount, getUser.name + "#" + getUser.discriminator, receiverId)
                            sqlCursor.execute(sql, val)

                        sql = 'UPDATE userDB SET coins = %s, userName = %s WHERE userId = %s'
                        val = (userData["coins"]-giveAmount, ctx.author.name + "#" + ctx.author.discriminator, userData["userId"])
                        sqlCursor.execute(sql, val)
                        sqlDb.commit()

                        await ctx.send(f'**🪙 {ctx.author.display_name}** gave **{"{:,}".format(giveAmount)}** coins to **{getUser.display_name}**!')