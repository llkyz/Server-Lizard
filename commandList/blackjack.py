import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import math
import random
import asyncio
from functions import *

def setup(client):
    @client.command(aliases=['bj','blackjack']) #!blackjack
    async def blacjack(ctx):
        userData = await checkAccount(ctx)
        bet = await checkBet(userData,ctx)

        if bet != None:

            cardTypes = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
            cardSuits = ["♣️","♦️","♥️","♠️"]
            cardValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
            playerHand = []
            dealerHand = []

            def drawCard(targetHand):
                myNum = random.randint(1,52)
                while ('id', myNum) in playerHand or ('id', myNum) in dealerHand:
                    myNum = random.randint(1,52)
                myCard = (myNum % 13) - 1
                mySuit = math.ceil(myNum / 13) - 1
                targetHand.append({'id': myNum, 'type': cardTypes[myCard], 'suit': cardSuits[mySuit], 'value': cardValues[myCard]})

            def printCards(targetHand):
                textOutput = []

                for x in targetHand:
                    textOutput.append(f'{x["type"]}{x["suit"]}')
                textOutput = ", ".join(textOutput)

                return textOutput

            def printValue(targetHand):
                totalValue = 0
                aceCount = 0

                for x in targetHand:
                    totalValue += x["value"]
                    if x["value"] == 1:
                        aceCount += 1

                if aceCount > 0 and totalValue < 12:
                    valueOutput = f'{totalValue} or {totalValue + 10}'
                    highestValue = totalValue + 10
                else:
                    valueOutput = f'{totalValue}'
                    highestValue = totalValue

                return valueOutput, highestValue

            def dealerDraw():
                while printValue(dealerHand)[1] < 17:
                    drawCard(dealerHand)
            
            drawCard(playerHand)
            drawCard(playerHand)
            drawCard(dealerHand)

            view = discord.ui.View()
            button1 = discord.ui.Button(label="Hit", style=ButtonStyle.green, custom_id='hit')
            button2 = discord.ui.Button(label="Stand", style=ButtonStyle.red, custom_id='stand')
            view.add_item(item=button1)
            view.add_item(item=button2)
            embed = discord.Embed(description=f'**[ Bet: 🪙 {"{:,}".format(bet)} ]**')
            embed.set_author(name=f'{ctx.author.display_name} is playing Blackjack', icon_url=ctx.author.display_avatar)
            embed.add_field(name=f'Dealer `[{printValue(dealerHand)[0]}]`', value=f'`{printCards(dealerHand)}, ??`', inline=True)
            embed.add_field(name=f'{ctx.author.display_name} `[{printValue(playerHand)[0]}]`', value=f'`{printCards(playerHand)}`', inline=True)
            msg1 = await ctx.send(embed=embed, view=view)

            def checkButton(m):
                return m.message == msg1 and m.user == ctx.author

            exitLoop = 0
            while exitLoop == 0:
                try:
                    interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                except asyncio.TimeoutError:
                    view.clear_items()
                    await msg1.edit(content='Timed out!', view=view)
                else:
                    await interacted.response.defer()
                    if interacted.data['custom_id'] == 'stand':
                        exitLoop = 1
                    elif interacted.data['custom_id'] == 'hit':
                        drawCard(playerHand)
                        if printValue(playerHand)[1] > 21:
                            exitLoop = 1
                        
                        embed_dict = embed.to_dict()
                        for field in embed_dict["fields"]:
                            if f'{ctx.author.display_name}' in field["name"]:
                                field["name"] = f'{ctx.author.display_name} `[{printValue(playerHand)[0]}]`'
                                field["value"] = f'`{printCards(playerHand)}`'

                        embed = discord.Embed.from_dict(embed_dict)
                        await msg1.edit(embed=embed)

            dealerDraw()

            playerValue = printValue(playerHand)[1]
            dealerValue = printValue(dealerHand)[1]
            if playerValue > 21:
                if dealerValue > 21:
                    result = 'tie'
                else:
                    result = 'lose'
            else:
                if dealerValue > 21:
                    result = 'win'
                elif playerValue == dealerValue:
                    result = 'tie'
                elif playerValue > dealerValue:
                    result = 'win'
                else:
                    result = 'lose'

            if result == 'win':
                resultText = 'You win!'
                color = 0x00FF00
            elif result == 'lose':
                resultText = 'You lose...'
                color = 0xFF5733
            else:
                resultText = 'It\'s a tie!'
                color = 0xaacbeb

            view = discord.ui.View()
            embed = discord.Embed(description=f'**[ Bet: 🪙 {"{:,}".format(bet)} ]** {resultText}',color=color)
            embed.set_author(name=f'{ctx.author.display_name} is playing Blackjack', icon_url=ctx.author.display_avatar)
            embed.add_field(name=f'Dealer `[{printValue(dealerHand)[1]}]`', value=f'`{printCards(dealerHand)}`', inline=True)
            embed.add_field(name=f'{ctx.author.display_name} `[{printValue(playerHand)[1]}]`', value=f'`{printCards(playerHand)}`', inline=True)
            await msg1.edit(embed=embed, view=view)

            updateCoins(userData, result, bet)