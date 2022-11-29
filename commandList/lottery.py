import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import random
import asyncio
from functions import *

docs = {

    "aliases":['4D', '4d'],

    "usage":"!lottery [bet] [4-digit number]",

    "description":"Choose a 4 digit number. If it matches any of the prize numbers, you win a huge payout!\nThe 'SMALL' prize category contains a First, Second, and Third prize. The 'BIG' category contains all 3 prizes, plus additional Starter and Consolation prizes.",

    "category":"gamble"
    
    }

def setup(client):
    @client.command(aliases=['4D','4d'])
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
    async def lottery(ctx):
        userData = await checkAccount(ctx)

        gameProceed = 0
        if userData != None:
                msgData = ctx.message.content.split(" ")
                if len(msgData) != 3:
                    await ctx.reply("Please use the following format: !lottery [bet] [4-digit number]", delete_after=20)
                else:
                    try:
                        bet = int(msgData[1])
                        choice = int(msgData[2])
                    except:
                        await ctx.reply("Please use the following format: !lottery [bet] [4-digit number]", delete_after=20)
                    else:
                        if bet > userData["coins"]:
                            await ctx.reply("You don't have enough coins to bet that much.", delete_after=20)
                        elif bet < 1:
                            await ctx.reply("You can't bet less than 1 coin!")
                        elif len(str(msgData[2])) != 4:
                            await ctx.reply("Please enter a 4 digit number to bet on.", delete_after=20)
                        else:
                            gameProceed = 1

        if gameProceed == 1:
            view = discord.ui.View()
            button1 = discord.ui.Button(label="Big", style=ButtonStyle.grey, custom_id='big')
            button2 = discord.ui.Button(label="Small", style=ButtonStyle.grey, custom_id='small')
            view.add_item(item=button1)
            view.add_item(item=button2)
            embed = discord.Embed(title=f'Betting on __{msgData[2]}__', description=f'**[ Bet: 🪙 {"{:,}".format(bet)} ]**')
            embed.set_author(name=f'{ctx.author.display_name} is playing Lottery (4D)', icon_url=ctx.author.display_avatar)
            embed.add_field(name=f'Prize Category', value=f'First\nSecond\nThird\nStarter\nConsolation', inline=True)
            embed.add_field(name=f'Big', value=f'2000x\n1000x\n490x\n250x\n60x', inline=True)
            embed.add_field(name=f'Small', value=f'3000x\n2000x\n800x\n-\n-', inline=True)
            msg1 = await ctx.send(embed=embed, view=view)

            def checkButton(m):
                return m.message == msg1 and m.user == ctx.author

            try:
                interacted = await client.wait_for('interaction', timeout=120, check=checkButton)
            except asyncio.TimeoutError:
                view.clear_items()
                await msg1.edit(content='Timed out!', view=view)
            else:
                await interacted.response.defer()
                prizeNumbers = []
                def rollNumber(rollCount):
                    for x in range(rollCount):
                        randomNumber = random.randint(0, 9999)
                        while randomNumber in prizeNumbers:
                            randomNumber = random.randint(0, 9999)
                        prizeNumbers.append(randomNumber)

                if interacted.data['custom_id'] == 'big':
                    betType = "big"
                    rollNumber(23)

                elif interacted.data['custom_id'] == 'small':
                    betType = "small"
                    rollNumber(3)

                def makeResultsTable():
                    prizeList = "**First Prize**\n"
                    strList = []
                    for x in range(len(prizeNumbers)):
                        if prizeNumbers[x] == choice:
                            strList.append(f'__**`{str(prizeNumbers[x]).zfill(4)}`**__')
                        else:
                            strList.append(f'`{str(prizeNumbers[x]).zfill(4)}`')
                    prizeList += strList[0] + "\n"
                    prizeList += "**Second Prize**\n" + strList[1] + "\n"
                    prizeList += "**Third Prize**\n" + strList[2] + "\n"
                    
                    if betType == "big":
                        prizeList += "**Starter Prize**\n"
                        prizeList += " ".join(strList[3:8]) + "\n"
                        prizeList += " ".join(strList[8:13]) + "\n"

                        prizeList += "**Consolation Prize**\n"
                        prizeList += " ".join(strList[13:18]) + "\n"
                        prizeList += " ".join(strList[18:24]) + "\n"
                    return prizeList

                multiplier = 1
                if choice not in prizeNumbers:
                    result = "lose"
                    resultText = "You didn't win..."
                else:
                    result = "win"

                    if prizeNumbers.index(choice) == 0:
                        prizeType = "First"
                        if betType == "big":
                            multiplier = 2000
                        else:
                            multiplier = 3000
                    elif prizeNumbers.index(choice) == 1:
                        prizeType = "Second"
                        if betType == "big":
                            multiplier = 1000
                        else:
                            multiplier = 2000
                    elif prizeNumbers.index(choice) == 2:
                        prizeType = "Third"
                        if betType == "big":
                            multiplier = 490
                        else:
                            multiplier = 800
                    elif prizeNumbers.index(choice) < 13:
                        prizeType = "Starter"
                        multiplier = 250
                    else:
                        prizeType = "Consolation"
                        multiplier = 60

                    resultText = f'🪙🪙 **You won the {prizeType} prize of {bet*multiplier} coins!** 🪙🪙'
                
                view.remove_item(item=button1)
                view.remove_item(item=button2)
                embed = discord.Embed(title=f'Betting on __{msgData[2]}__', description=f'**[ Bet: 🪙 {"{:,}".format(bet)} ]** {resultText}')
                embed.set_author(name=f'{ctx.author.display_name} is playing Lottery (4D)', icon_url=ctx.author.display_avatar)
                embed.add_field(name=f'Prize Category', value=f'First\nSecond\nThird\nStarter\nConsolation', inline=True)
                embed.add_field(name=f'Big', value=f'2000x\n1000x\n490x\n250x\n60x', inline=True)
                embed.add_field(name=f'Small', value=f'3000x\n2000x\n800x\n-\n-', inline=True)
                embed.add_field(name=f'__**Results**__', value=makeResultsTable(), inline=False)
                await msg1.edit(embed=embed, view=view)

                updateCoins(userData, result, bet*multiplier)