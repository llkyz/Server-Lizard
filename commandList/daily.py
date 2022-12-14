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
    @commands.cooldown(1,15,commands.BucketType.user)
    async def daily(ctx):
        userData = await fetchUserData(ctx.author)
        coinEmoji = checkGoldenLizard(userData)
        if userData != None:
            sqlCursor.execute('SELECT CURDATE()')
            currentDate = sqlCursor.fetchone()[0]
            if str(currentDate) != userData["daily"]:
                dailyCoins = random.randint(500,2000)

                sql = 'UPDATE userDB SET coins = %s, daily = %s WHERE userId = %s'
                val = (userData["coins"]+dailyCoins, str(currentDate), userData["userId"])
                sqlCursor.execute(sql, val)
                sqlDb.commit()

                await ctx.send(f'{coinEmoji} **| {ctx.author.display_name}** You got **{"{:,}".format(dailyCoins)}** coins!')
            else:
                await ctx.send(f'{coinEmoji} **| {ctx.author.display_name}**  You already claimed your daily coins!', delete_after=20)