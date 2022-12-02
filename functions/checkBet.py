import discord
from discord.ext import commands

async def checkBet(userData, arg, ctx):
    if userData != None:
        if arg == None:
            if userData["coins"] > 0:
                return 1
            else:
                await ctx.reply("You don't have any coins to bet!", delete_after=20)
        else:
            if arg[-1] == "k".casefold():
                multiplier = 1000
                arg = arg[:-1]
            elif arg[-1] == "m".casefold():
                multiplier = 1000000
                arg = arg[:-1]
            else:
                multiplier = 1

            try:
                query = int(float(arg.replace(",","")) * multiplier)
            except:
                await ctx.reply("Please enter a proper bet amount.", delete_after=20)
            else:
                if query > userData["coins"]:
                    await ctx.reply("You don't have enough coins to bet that much.", delete_after=20)
                elif query < 1:
                    await ctx.reply("You can't bet less than 1 coin!", delete_after=20)
                else:
                    return query