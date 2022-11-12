import discord
from discord.ext import commands

async def checkBet(userData,ctx):
    if userData != None:
        msgData = ctx.message.content.split(" ")
        if len(msgData) == 1:
            if userData["money"] > 0:
                return 1
            else:
                await ctx.reply("You don't have any coins to bet!")
        else:
            try:
                query = int(msgData[1])
            except:
                await ctx.reply("Please enter a proper bet amount.")
            else:
                if query > userData["money"]:
                    await ctx.reply("You don't have enough coins to bet that much.")
                elif query < 1:
                    await ctx.reply("You can't bet less than 1 coin!")
                else:
                    return query