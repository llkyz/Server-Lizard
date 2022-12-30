import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import asyncio
from functions import *
import random

docs = {

    "aliases":['battleblackjack'],

    "usage":"!battlebj [@user] [optional: bet]",

    "description":"Play against another user in a battle of Blackjack!",

    "category":"games"
    
    }

def setup(client):
    @client.command(aliases=['battleblackjack']) #!battle
    async def battlebj(ctx, arg=None, arg2=None):
        if arg == None:
            await ctx.reply('Invalid syntax! Please use `!battlerps [@user] [optional: bet]`', delete_after=20)
            return

        try:
            opponentId = int(arg.replace('<@','').replace('>',''))
            guild = await client.fetch_guild(ctx.guild.id)
            opponent = await guild.fetch_member(opponentId)
        except:
            await ctx.reply('Invalid syntax! Please use `!battle [@user] [optional: bet]`', delete_after=20)
            return

        if ctx.guild.get_member(opponentId) is None:
            await ctx.reply('Invalid syntax! Please use `!battlerps [@user] [optional: bet]`', delete_after=20)
            return
        elif opponent.id == 1032276665092538489:
            await ctx.reply('Use !rps for a regular RPS game!', delete_after=20)
            return
        elif opponent == ctx.author:
            await ctx.reply('You cannot battle yourself!', delete_after=20)
            return

        if arg2 != None:
            userData = await fetchUserData(ctx.author)
            bet = await checkBet(userData, arg2, ctx)
            if bet == -1:
                return
            else:
                updateCoins(ctx.author.id, -bet)
        else:
            bet = 0

        view = discord.ui.View()
        button1 = discord.ui.Button(label="Accept", style=ButtonStyle.green, custom_id='accept')
        button2 = discord.ui.Button(label="Decline", style=ButtonStyle.red, custom_id='decline')
        view.add_item(item=button1)
        view.add_item(item=button2)
        embed = discord.Embed(title=f'Blackjack', description=f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]**', color=0xaacbeb)
        embed.set_author(name=f'{ctx.author.display_name} vs {opponent.display_name}', icon_url=ctx.author.display_avatar)
        mymsg = await ctx.reply(content=f'{opponent.display_name}, {ctx.author.display_name} wants to battle!', embed=embed, view=view)

        def checkButton(m):
            return m.message == mymsg and m.user.id == opponentId

        try:
            interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
        except asyncio.TimeoutError:
            await mymsg.edit(content='Timed out!', view=None)
            updateCoins(ctx.author.id, bet)
            return

        if interacted.data['custom_id'] == 'decline':
            await interacted.response.defer()
            await mymsg.edit(view=None)
            await mymsg.reply(content='Battle declined.')
            updateCoins(ctx.author.id, bet)
            return

        await interacted.response.defer()

        opponentData = await fetchUserData(opponent)
        if await checkBet(opponentData, arg2, ctx) == None:
            updateCoins(ctx.author.id, bet)
            return
        updateCoins(opponentId, -bet)
        
        cardback = "<:cardback:1047469347586711552>"
        cards = ["blank","<:c_ace:1047469363189526549>","<:c_two:1047469380470059138>","<:c_three:1047469391098413098>","<:c_four:1047469399977758740>","<:c_five:1047469407049367632>","<:c_six:1047469418046820372>","<:c_seven:1047469424732553287>","<:c_eight:1047469432257118250>","<:c_nine:1047469439450370068>","<:c_ten:1047469452603686983>","<:c_jack:1047469553707397213>","<:c_queen:1047469567255003166>","<:c_king:1047469573974278144>","<:d_ace:1047469624679202866>","<:d_two:1047469634120585226>","<:d_three:1047469640588214282>","<:d_four:1047469647315882004>","<:d_five:1047469653238235146>","<:d_six:1047469659659702302>","<:d_seven:1047469665938587759>","<:d_eight:1047469672251011142>","<:d_nine:1047469680576700457>","<:d_ten:1047469691767115776>","<:d_jack:1047469908289658961>","<:d_queen:1047469915633897502>","<:d_king:1047469924077031524>","<:h_ace:1047470468107616286>","<:h_two:1047470477829996604>","<:h_three:1047470485023236166>","<:h_four:1047470491386003537>","<:h_five:1047470497677443102>","<:h_six:1047470510797230080>","<:h_seven:1047470517713645638>","<:h_eight:1047470525565374544>","<:h_nine:1047470537946968115>","<:h_ten:1047470545089855528>","<:h_jack:1047470552975159296>","<:h_queen:1047470564148772926>","<:h_king:1047470572499636314>","<:s_ace:1047470673133572176>","<:s_two:1047470680544915466>","<:s_three:1047470686567944233>","<:s_four:1047470693211721790>","<:s_five:1047470699498967070>","<:s_six:1047470705924653117>","<:s_seven:1047470712841060432>","<:s_eight:1047487024040513637>","<:s_nine:1047487043036520468>","<:s_ten:1047487052373032960>","<:s_jack:1047471402258800640>","<:s_queen:1047471423347773441>","<:s_king:1047471433523138660>"]

        cardValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        userHand = []
        opponentHand = []

        def drawCard(targetHand):
                myNum = random.randint(1,52)
                while (myNum) in userHand or (myNum) in opponentHand:
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

        drawCard(userHand)
        drawCard(userHand)
        drawCard(opponentHand)
        drawCard(opponentHand)

        button1 = discord.ui.Button(label="View Hand", style=ButtonStyle.grey, custom_id='view')
        button2 = discord.ui.Button(label="Hit", style=ButtonStyle.green, custom_id='hit')
        button3 = discord.ui.Button(label="Stand", style=ButtonStyle.red, custom_id='stand')
        view.clear_items()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)

        gameBoardEmbed = discord.Embed(description=f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]**\n\nWaiting for players to draw:',color=0xaacbeb)
        gameBoardEmbed.set_author(name=f'{ctx.author.display_name} vs {opponent.display_name}', icon_url=ctx.author.display_avatar)
        gameBoardEmbed.add_field(name=f'> {ctx.author.display_name}', value=cardback*len(userHand), inline=True)
        gameBoardEmbed.add_field(name=f'> {opponent.display_name}', value=cardback*len(opponentHand), inline=True)
        await mymsg.edit(content=None, embed=gameBoardEmbed, view=view)

        def checkPlayer(m):
            return m.message == mymsg and m.user in remainingPlayers

        remainingPlayers = [ctx.author, opponent]
        while len(remainingPlayers) != 0:
            try:
                interacted = await client.wait_for('interaction', timeout=300, check=checkPlayer)
            except asyncio.TimeoutError:
                remainingPlayers = []
            else:
                if interacted.user == ctx.author:
                    if interacted.data['custom_id'] == 'view':
                        content = "Viewing Hand"
                        embed = discord.Embed(title="Current Hand", description=f'Value: `[{printValue(userHand)[0]}]`\n\n{printCards(userHand)}')
                        await interacted.response.send_message(content=content, embed=embed, ephemeral=True)

                    elif interacted.data['custom_id'] == 'hit':
                        drawCard(userHand)
                        if printValue(userHand)[1] > 21:
                            content = "Bust! Please wait for your opponent to complete their hand..."
                            embed = discord.Embed(title="Current Hand", description=f'Value: `[{printValue(userHand)[1]}]`\n\n{printCards(userHand)}')
                            remainingPlayers.remove(ctx.author)
                        else:
                            content = "Drew a card"
                            embed = discord.Embed(title="Current Hand", description=f'Value: `[{printValue(userHand)[0]}]`\n\n{printCards(userHand)}')

                        await interacted.response.send_message(content=content, embed=embed, ephemeral=True)
                        gameBoardEmbed.set_field_at(index=0, name=f'> {ctx.author.display_name}', value=cardback*len(userHand), inline=True)
                        await mymsg.edit(embed=gameBoardEmbed)
                        
                    elif interacted.data['custom_id'] == 'stand':
                        content = "Waiting for opponent to complete their hand..."
                        embed = discord.Embed(title="Current Hand", description=f'Value: `[{printValue(userHand)[1]}]`\n\n{printCards(userHand)}')
                        await interacted.response.send_message(content=content, embed=embed, ephemeral=True)
                        remainingPlayers.remove(ctx.author)
            
                if interacted.user == opponent:
                        if interacted.data['custom_id'] == 'view':
                            content = "Viewing Hand"
                            embed = discord.Embed(title="Current Hand", description=f'Value: `[{printValue(opponentHand)[0]}]`\n\n{printCards(opponentHand)}')
                            await interacted.response.send_message(content=content, embed=embed, ephemeral=True)

                        elif interacted.data['custom_id'] == 'hit':
                            drawCard(opponentHand)
                            if printValue(opponentHand)[1] > 21:
                                content = "Bust! Please wait for your opponent to complete their hand..."
                                embed = discord.Embed(title="Current Hand", description=f'Value: `[{printValue(opponentHand)[1]}]`\n\n{printCards(opponentHand)}')
                                remainingPlayers.remove(opponent)
                            else:
                                content = "Drew a card"
                                embed = discord.Embed(title="Current Hand", description=f'Value: `[{printValue(opponentHand)[0]}]`\n\n{printCards(opponentHand)}')

                            await interacted.response.send_message(content=content, embed=embed, ephemeral=True)
                            gameBoardEmbed.set_field_at(index=1, name=f'> {opponent.display_name}', value=cardback*len(opponentHand), inline=True)
                            await mymsg.edit(embed=gameBoardEmbed)
                            
                        elif interacted.data['custom_id'] == 'stand':
                            content = "Waiting for opponent to complete their hand..."
                            embed = discord.Embed(title="Current Hand", description=f'Value: `[{printValue(opponentHand)[1]}]`\n\n{printCards(opponentHand)}')
                            await interacted.response.send_message(content=content, embed=embed, ephemeral=True)
                            remainingPlayers.remove(opponent)
        
        await mymsg.edit(view=None)

        userValue = printValue(userHand)[1]
        opponentValue = printValue(opponentHand)[1]
        if userValue > 21:
            if opponentValue > 21:
                result = 'tie'
            else:
                result = 'lose'
        else:
            if opponentValue > 21:
                result = 'win'
            elif userValue == opponentValue:
                result = 'tie'
            elif userValue > opponentValue:
                result = 'win'
            else:
                result = 'lose'

        if result == 'tie':
            title = 'It\'s a tie!'
            icon = client.user.display_avatar
        elif result == 'win':
            title = f'{ctx.author.display_name} wins!'
            icon = ctx.author.display_avatar
        elif result == 'lose':
            title = f'{opponent.display_name} wins!'
            icon = opponent.display_avatar

        embed = discord.Embed(description=f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]**',color=0xaacbeb)
        embed.set_author(name=title, icon_url=icon)
        embed.add_field(name=f'> {ctx.author.display_name}', value=f'`[{printValue(userHand)[1]}]` {printCards(userHand)}', inline=True)
        embed.add_field(name=f'> {opponent.display_name}', value=f'`[{printValue(opponentHand)[1]}]` {printCards(opponentHand)}', inline=True)
        await ctx.send(embed=embed)

        if bet != 0:
            if result == "win":
                updateCoins(ctx.author.id, bet*2)
            elif result == "tie":
                updateCoins(ctx.author.id, bet)
                updateCoins(opponentId, bet)
            else:
                updateCoins(opponentId, bet*2)