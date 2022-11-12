import discord
from discord.ext import commands
import random
from functions import *


def setup(client):
    @client.command() # Get a random number of coins every day
    async def daily(ctx):
        userData = await checkAccount(ctx)
        if userData != None:
            sqlCursor.execute('SELECT CURDATE()')
            currentDate = sqlCursor.fetchone()[0]
            if str(currentDate) != userData["daily"]:
                dailyCoins = random.randint(500,2000)

                sql = 'UPDATE userDB SET coins = %s, daily = %s WHERE userId = %s'
                val = (userData["money"]+dailyCoins, currentDate, userData["id"])
                sqlCursor.execute(sql, val)
                sqlDb.commit()

                await ctx.reply(f'You got {dailyCoins} coins!')
            else:
                await ctx.reply(f'You already claimed your daily coins!')