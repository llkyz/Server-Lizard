import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import math
import random
import asyncio
from functions import *
import json

docs = {

    "aliases":['bj', 'breadjack'],

    "usage":"!blackjack [bet]",

    "description":"Play a game of Blackjack!\n\nGet the highest hand value without exceeding 21. Double your bet if you win!\nIf you choose to forfeit, you'll get back 50% of your bet.",

    "category":"gamble"
    
    }


cardback = "<:cardback:1047469347586711552>"
cards = ["blank","<:c_ace:1047469363189526549>","<:c_two:1047469380470059138>","<:c_three:1047469391098413098>","<:c_four:1047469399977758740>","<:c_five:1047469407049367632>","<:c_six:1047469418046820372>","<:c_seven:1047469424732553287>","<:c_eight:1047469432257118250>","<:c_nine:1047469439450370068>","<:c_ten:1047469452603686983>","<:c_jack:1047469553707397213>","<:c_queen:1047469567255003166>","<:c_king:1047469573974278144>","<:d_ace:1047469624679202866>","<:d_two:1047469634120585226>","<:d_three:1047469640588214282>","<:d_four:1047469647315882004>","<:d_five:1047469653238235146>","<:d_six:1047469659659702302>","<:d_seven:1047469665938587759>","<:d_eight:1047469672251011142>","<:d_nine:1047469680576700457>","<:d_ten:1047469691767115776>","<:d_jack:1047469908289658961>","<:d_queen:1047469915633897502>","<:d_king:1047469924077031524>","<:h_ace:1047470468107616286>","<:h_two:1047470477829996604>","<:h_three:1047470485023236166>","<:h_four:1047470491386003537>","<:h_five:1047470497677443102>","<:h_six:1047470510797230080>","<:h_seven:1047470517713645638>","<:h_eight:1047470525565374544>","<:h_nine:1047470537946968115>","<:h_ten:1047470545089855528>","<:h_jack:1047470552975159296>","<:h_queen:1047470564148772926>","<:h_king:1047470572499636314>","<:s_ace:1047470673133572176>","<:s_two:1047470680544915466>","<:s_three:1047470686567944233>","<:s_four:1047470693211721790>","<:s_five:1047470699498967070>","<:s_six:1047470705924653117>","<:s_seven:1047470712841060432>","<:s_eight:1047487024040513637>","<:s_nine:1047487043036520468>","<:s_ten:1047487052373032960>","<:s_jack:1047471402258800640>","<:s_queen:1047471423347773441>","<:s_king:1047471433523138660>"]

def setup(client):
    @client.command(aliases=['bj', 'breadjack'])
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
    async def blackjack(ctx, arg=None):
        userData = await fetchUserData(ctx.author)
        bet = await checkBet(userData, arg, ctx)

        if bet != None:
            cardValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
            playerHand = []
            dealerHand = []

            def drawCard(targetHand):
                myNum = random.randint(1,52)
                while (myNum) in playerHand or (myNum) in dealerHand:
                    myNum = random.randint(1,52)
                targetHand.append(myNum)

            def printCards(targetHand):
                cardOutput = []

                for x in targetHand:
                    cardOutput.append(cards[x])
                cardOutput = " ".join(cardOutput)

                return cardOutput

            def printValue(targetHand):
                totalValue = 0
                aceCount = 0

                for x in targetHand:
                    totalValue += cardValues[(x % 13) - 1]
                    if cardValues[(x % 13) - 1] == 1:
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

            if userData["bjPlayer"] == None and userData["bjDealer"] == None:
                drawCard(playerHand)
                drawCard(playerHand)
                drawCard(dealerHand)
                updateCoins(ctx.author.id, -bet)
                sql = 'UPDATE userDB SET bjBet = %s WHERE userId = %s'
                val = (bet, ctx.author.id)
                sqlCursor.execute(sql, val)
                sqlDb.commit()
                resumeText = ""
            else:
                dealerHand = json.loads(userData["bjDealer"])
                playerHand = json.loads(userData["bjPlayer"])
                bet = userData["bjBet"]
                resumeText = "Resuming previous Blackjack game..."
                
            view = discord.ui.View()
            button1 = discord.ui.Button(label="Hit", style=ButtonStyle.green, custom_id='hit')
            button2 = discord.ui.Button(label="Stand", style=ButtonStyle.red, custom_id='stand')
            button3 = discord.ui.Button(label="Forfeit", style=ButtonStyle.blurple, custom_id='forfeit')
            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button3)
            embed = discord.Embed(description=f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]**')
            embed.set_author(name=f'{ctx.author.display_name} is playing Blackjack', icon_url=ctx.author.display_avatar)
            embed.add_field(name=f'Dealer `[{printValue(dealerHand)[0]}]`', value=f'{printCards(dealerHand)} {cardback}', inline=True)
            embed.add_field(name=f'{ctx.author.display_name} `[{printValue(playerHand)[0]}]`', value=f'{printCards(playerHand)}', inline=True)
            msg1 = await ctx.send(content=resumeText, embed=embed, view=view)

            def checkButton(m):
                return m.message == msg1 and m.user == ctx.author

            while True:
                sql = 'UPDATE userDB SET bjDealer = %s, bjPlayer = %s WHERE userId = %s'
                val = (json.dumps(dealerHand), json.dumps(playerHand), ctx.author.id)
                sqlCursor.execute(sql, val)
                sqlDb.commit()

                try:
                    interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                except asyncio.TimeoutError:
                    await msg1.edit(content='Timed out!', view=None)
                    return
                else:
                    await interacted.response.defer()
                    if interacted.data['custom_id'] == 'stand':
                        break
                    elif interacted.data['custom_id'] == 'hit':
                        drawCard(playerHand)
                        if printValue(playerHand)[1] > 21:
                            break
                        
                        embed_dict = embed.to_dict()
                        for field in embed_dict["fields"]:
                            if f'{ctx.author.display_name}' in field["name"]:
                                field["name"] = f'{ctx.author.display_name} `[{printValue(playerHand)[0]}]`'
                                field["value"] = f'{printCards(playerHand)}'

                        embed = discord.Embed.from_dict(embed_dict)
                        await msg1.edit(embed=embed)

                    elif interacted.data['custom_id'] == 'forfeit':
                        resultText = f'Hand Forfeited! You get back {"{:,}".format(math.floor(bet/2))} coins'

                        embed_dict = embed.to_dict()
                        embed_dict["description"] = f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]** {resultText}'
                        embed_dict["color"] = 0xFF5733
                        embed = discord.Embed.from_dict(embed_dict)
                        await msg1.edit(embed=embed, view=None)

                        sql = 'UPDATE userDB SET bjDealer = %s, bjPlayer = %s, bjBet = %s WHERE userId = %s'
                        val = (None, None, None, ctx.author.id)
                        sqlCursor.execute(sql, val)
                        sqlDb.commit()

                        updateCoins(ctx.author.id, math.floor(bet/2))
                        return
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
            embed = discord.Embed(description=f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]** {resultText}',color=color)
            embed.set_author(name=f'{ctx.author.display_name} is playing Blackjack', icon_url=ctx.author.display_avatar)
            embed.add_field(name=f'Dealer `[{printValue(dealerHand)[1]}]`', value=f'{printCards(dealerHand)}', inline=True)
            embed.add_field(name=f'{ctx.author.display_name} `[{printValue(playerHand)[1]}]`', value=f'{printCards(playerHand)}', inline=True)
            await msg1.edit(embed=embed, view=view)

            sql = 'UPDATE userDB SET bjDealer = %s, bjPlayer = %s, bjBet = %s WHERE userId = %s'
            val = (None, None, None, ctx.author.id)
            sqlCursor.execute(sql, val)
            sqlDb.commit()

            if result == "win":
                updateCoins(ctx.author.id, bet*2)
            elif result == "tie":
                updateCoins(ctx.author.id, bet)