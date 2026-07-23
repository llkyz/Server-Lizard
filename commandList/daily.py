import discord
from discord.ext import commands
import random
from functions import *
from functions.sql_start import SQLObject

docs = {

    "aliases":[],

    "usage":"!daily",

    "description":"Get a random amount of free coins every day! Resets at UTC midnight.",

    "category":"economy"
    
    }

async def setup(client):
    @client.command()
    @commands.cooldown(1,15,commands.BucketType.user)
    async def daily(ctx):
        userData = await fetchUserData(ctx.author)
        coinEmoji = checkGoldenLizard(userData)
        if userData != None:
            SQLObject.execute('SELECT CURDATE()')
            currentDate = SQLObject.fetchone()[0]
            if str(currentDate) != userData["daily"]:
                dailyCoins = random.randint(500,2000)

                sql = 'UPDATE userDB SET coins = %s, daily = %s WHERE userId = %s'
                val = (userData["coins"]+dailyCoins, str(currentDate), userData["userId"])
                SQLObject.execute(sql, val)
                SQLObject.commit()

                await ctx.send(f'{coinEmoji} **| {ctx.author.display_name}** You got **{"{:,}".format(dailyCoins)}** coins!')
            else:
                await ctx.send(f'{coinEmoji} **| {ctx.author.display_name}**  You already claimed your daily coins!', delete_after=20)