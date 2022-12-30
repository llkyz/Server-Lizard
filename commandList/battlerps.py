import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import asyncio
from functions import *

docs = {

    "aliases":[],

    "usage":"!battlerps [@user] [optional: bet]",

    "description":"Play against another user in a battle of Rock Paper Scissors!",

    "category":"games"
    
    }

def setup(client):
    @client.command() #!battle
    async def battlerps(ctx, arg=None, arg2=None):
        if arg == None:
            await ctx.reply('Invalid syntax! Please use `!battlerps [@user] [optional: bet]`', delete_after=20)
            return
        else:
            try:
                opponentId = int(arg.replace('<@','').replace('>',''))
                guild = await client.fetch_guild(ctx.guild.id)
                opponent = await guild.fetch_member(opponentId)
            except:
                await ctx.reply('Invalid syntax! Please use `!battle [@user] [optional: bet]`', delete_after=20)
                return
            else:
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
                embed = discord.Embed(title=f'Rock Paper Scissors 🗿📰✂', description=f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]**', color=0xaacbeb)
                embed.set_author(name=f'{ctx.author.display_name} vs {opponent.display_name}', icon_url=ctx.author.display_avatar)
                mymsg = await ctx.reply(content=f'{opponent.display_name}, {ctx.author.display_name} wants to battle!', embed=embed, view=view)

                def checkButton(m):
                    return m.message == mymsg and m.user.id == opponentId

                try:
                    interacted = await client.wait_for('interaction', timeout=120, check=checkButton)
                except asyncio.TimeoutError:
                    await mymsg.edit(content='Timed out!', view=None)
                    updateCoins(ctx.author.id, bet)
                    return
                else:
                    if interacted.data['custom_id'] == 'decline':
                        await interacted.response.defer()
                        await mymsg.edit(view=None)
                        await mymsg.reply(content='Battle declined.')
                        updateCoins(ctx.author.id, bet)
                        return

                    else:
                        await interacted.response.defer()
                        await mymsg.edit(view=None)

                        
                        opponentData = await fetchUserData(opponent)
                        if await checkBet(opponentData, arg2, ctx) == None:
                            updateCoins(ctx.author.id, bet)
                            return
                        updateCoins(opponentId, -bet)
                        
                        button1 = discord.ui.Button(label="Scissors ✂", style=ButtonStyle.grey, custom_id='scissors')
                        button2 = discord.ui.Button(label="Paper 📰", style=ButtonStyle.grey, custom_id='paper')
                        button3 = discord.ui.Button(label="Stone 🗿", style=ButtonStyle.grey, custom_id='stone')
                        view.clear_items()
                        view.add_item(button1)
                        view.add_item(button2)
                        view.add_item(button3)
                        embed = discord.Embed(description=f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]**\n\nWaiting for players to pick:',color=0xaacbeb)
                        embed.set_author(name=f'{ctx.author.display_name} vs {opponent.display_name}', icon_url=ctx.author.display_avatar)
                        embed.add_field(name="Player 1", value=f'> {ctx.author.display_name}', inline=True)
                        embed.add_field(name="Player 2", value=f'> {opponent.display_name}', inline=True)
                        await mymsg.edit(content=None, embed=embed, view=view)

                        remainingPlayers = [ctx.author, opponent]

                        def checkPlayer(m):
                            return m.message == mymsg and m.user in remainingPlayers
                        while len(remainingPlayers) != 0:
                            try:
                                interacted = await client.wait_for('interaction', timeout=300, check=checkPlayer)
                            except asyncio.TimeoutError:
                                await mymsg.edit(content='Timed out!', view=None)
                                updateCoins(ctx.author.id, bet)
                                updateCoins(opponentId, bet)
                                return
                            else:
                                await interacted.response.defer()
                                if interacted.user == ctx.author:
                                    remainingPlayers.remove(ctx.author)
                                    if interacted.data['custom_id'] == 'scissors':
                                        player1Choice = 0
                                    elif interacted.data['custom_id'] == 'paper':
                                        player1Choice = 1
                                    elif interacted.data['custom_id'] == 'stone':
                                        player1Choice = 2
                                    embed.set_field_at(index=0, name="Player 1", value=f'> {ctx.author.display_name} ✅', inline=True)
                                elif interacted.user == opponent:
                                    remainingPlayers.remove(opponent)
                                    if interacted.data['custom_id'] == 'scissors':
                                        player2Choice = 0
                                    elif interacted.data['custom_id'] == 'paper':
                                        player2Choice = 1
                                    elif interacted.data['custom_id'] == 'stone':
                                        player2Choice = 2
                                    embed.set_field_at(index=1, name="Player 2", value=f'> {opponent.display_name} ✅', inline=True)
                                await mymsg.edit(embed=embed)

                        choices = ['Scissors ✂', 'Paper 📰', 'Rock 🗿']
                        if (player1Choice == player2Choice):
                            result = "tie"
                            text = f'Both players chose **{choices[player1Choice]}**!'
                        else:
                            text = f'{ctx.author.display_name} chose **{choices[player1Choice]}** and {opponent.display_name} chose **{choices[player2Choice]}**!'
                            if (player1Choice == 0):
                                if (player2Choice == 1):
                                    result = "win"
                                else:
                                    result = "lose"
                            elif (player1Choice == 1):
                                if (player2Choice == 0):
                                    result = "lose"
                                else:
                                    result = "win"
                            else:
                                if (player2Choice == 0):
                                    result = "win"
                                else:
                                    result = "lose"

                        if result == 'tie':
                            title = 'It\'s a tie!'
                            icon = client.user.display_avatar
                        elif result == 'win':
                            title = f'{ctx.author.display_name} wins!'
                            icon = ctx.author.display_avatar
                        elif result == 'lose':
                            title = f'{opponent.display_name} wins!'
                            icon = opponent.display_avatar
                        
                        embed=discord.Embed(description=f'**[ Bet: <:lizard_coin:1047527590677712896> {"{:,}".format(bet)} ]**\n\n{text}', color=0xaacbeb)
                        embed.set_author(name=title, icon_url=icon)
                        await mymsg.edit(embed=embed, view=None)

                        if bet != 0:
                            if result == "win":
                                updateCoins(ctx.author.id, bet*2)
                            elif result == "tie":
                                updateCoins(ctx.author.id, bet)
                                updateCoins(opponentId, bet)
                            else:
                                updateCoins(opponentId, bet*2)