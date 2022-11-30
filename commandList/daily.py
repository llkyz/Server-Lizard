import discord
from discord.ext import commands
import random
from functions import *

docs = {

    "aliases":[],

    "usage":"!daily",

    "description":"Get a random amount of free coins every day! Resets at UTC midnight.",

    "category":"economy"
    
    }

def setup(client):
    @client.command()
    async def daily(ctx):
        userData = await fetchUserData(ctx.author)
        if userData != None:
            sqlCursor.execute('SELECT CURDATE()')
            currentDate = sqlCursor.fetchone()[0]
            if str(currentDate) != userData["daily"]:
                dailyCoins = random.randint(500,2000)

                sql = 'UPDATE userDB SET coins = %s, daily = %s WHERE userId = %s'
                val = (userData["coins"]+dailyCoins, currentDate, userData["userId"])
                sqlCursor.execute(sql, val)
                sqlDb.commit()

                await ctx.send(f'**{ctx.author.display_name} <:lizard_coin:1047527590677712896> |** You got **{"{:,}".format(dailyCoins)}** coins!')
            else:
                await ctx.send(f'**{ctx.author.display_name} <:lizard_coin:1047527590677712896> |** You already claimed your daily coins!', delete_after=20)