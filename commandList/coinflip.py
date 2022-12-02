import discord
from discord.ext import commands
import random
from discord import Button, ButtonStyle
import asyncio
from functions import *

docs = {

    "aliases":['cf'],

    "usage":"!coinflip [bet] [optional: heads(h) / tails(t)]",

    "description":"Flip a coin and pray to lady luck! Double your bet if you guessed it right, or lose it all...",

    "category":"gamble"
    
    }

def setup(client):
    @client.command(aliases=['cf'])
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
    async def coinflip(ctx, arg=None):
        userData = await fetchUserData(ctx.author)
        bet = await checkBet(userData, arg, ctx)

        if bet != None:
                sql = 'UPDATE userDB SET cfBet = %s WHERE userId = %s'
                val = (True, ctx.author.id)
                sqlCursor.execute(sql, val)
                sqlDb.commit()

                msgData = ctx.message.content.split(" ")
                if len(msgData) == 3:
                    match msgData[2]:
                        case "heads":
                            choice = 1
                        case "head":
                            choice = 1
                        case "h":
                            choice = 1
                        case "tails":
                            choice = 0
                        case "tail":
                            choice = 0
                        case "t":
                            choice = 0
                        case _:
                            choice = 1
                else:
                    choice = 1

                if choice == 1:
                    choiceText = "Heads"
                else:
                    choiceText = "Tails"
            
                embed=discord.Embed(title=f'Betting on {choiceText}', description=f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]** Flipping! Cross your fingers...', color=0xaacbeb)
                embed.set_author(name=f'{ctx.author.display_name} is playing Coin Flip', icon_url=ctx.author.display_avatar)
                msg1 = await ctx.send(embed=embed)

                await asyncio.sleep(2.5)

                coinResult = random.randint(0,1)

                if coinResult == 1:
                    coinResultText = "HEADS"
                else:
                    coinResultText = "TAILS"

                if coinResult == choice:
                    result = 'win'
                    resultText = "YOU WON!"
                    color = 0x00FF00
                else:
                    result = 'lose'
                    resultText = "You lost..."
                    color = 0xFF5733

                embed=discord.Embed(title=f'Betting on {choiceText}', description=f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]** **{coinResultText}!!** {resultText}', color=color)
                embed.set_author(name=f'{ctx.author.display_name} is playing Coin Flip', icon_url=ctx.author.display_avatar)
                await msg1.edit(embed=embed)

                sql = 'UPDATE userDB SET cfBet = %s WHERE userId = %s'
                val = (None, ctx.author.id)
                sqlCursor.execute(sql, val)
                sqlDb.commit()

                updateCoins(userData, result, bet)