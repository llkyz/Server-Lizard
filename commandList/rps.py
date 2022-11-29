import discord
from discord.ext import commands
import random
from discord import Button, ButtonStyle
import asyncio
from functions import *

docs = {

    "aliases":[],

    "usage":"!rps [bet]",

    "description":"Bet on a game of Rock Paper Scissors! Rock beats scissors, scissors beat paper, and paper beats rock.",

    "category":"gamble"
    
    }

def setup(client):
    @client.command()
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
    async def rps(ctx):
        userData = await checkAccount(ctx)
        bet = await checkBet(userData,ctx)

        if bet != None:

            view = discord.ui.View()
            button1 = discord.ui.Button(label="Rock 🗿", style=ButtonStyle.grey, custom_id='rock')
            button2 = discord.ui.Button(label="Paper 📰", style=ButtonStyle.grey, custom_id='paper')
            button3 = discord.ui.Button(label="Scissors ✂", style=ButtonStyle.grey, custom_id='scissors')
            view.add_item(item=button1)
            view.add_item(item=button2)
            view.add_item(item=button3)
            embed=discord.Embed(description=f'**[ Bet: 🪙 {"{:,}".format(bet)} ]** Pick your choice!')
            embed.set_author(name=f'{ctx.author.display_name} is playing Rock, Paper, Scissors', icon_url=ctx.author.display_avatar)
            msg = await ctx.send(embed=embed, view=view)

            def check(m):
                return m.message == msg and m.user == ctx.author

            try:
                interacted = await client.wait_for('interaction', timeout=120, check=check)
            except asyncio.TimeoutError:
                button1.disabled = True
                button2.disabled = True
                button3.disabled = True
                await msg.edit(content='Timed out!', view=view)
            else:
                await interacted.response.defer()

                choices = ['Rock', 'Paper', 'Scissors']
                emoji = ['🗿 Rock','📰 Paper','✂ Scissors']
                
                if interacted.data['custom_id'] == 'rock':
                    playerChoice = 0
                elif interacted.data['custom_id'] == 'paper':
                    playerChoice = 1
                elif interacted.data['custom_id'] == 'scissors':
                    playerChoice = 2
                    
                computerChoice = random.randint(0,2)
                
                if (playerChoice == computerChoice):
                    result = 'tie'
                else:
                    if (playerChoice == 0):
                        if (computerChoice == 1):
                            result = 'lose'
                        else:
                            result = 'win'
                    elif (playerChoice == 1):
                        if (computerChoice == 0):
                            result = 'win'
                        else:
                            result = 'lose'
                    else:
                        if (computerChoice == 0):
                            result = 'lose'
                        else:
                            result = 'win'

                if result == 'win':
                    resultText = 'You win!'
                    color = 0x00FF00
                elif result == 'lose':
                    resultText = 'You lose...'
                    color = 0xFF5733
                else:
                    resultText = 'It\'s a tie!'
                    color = 0xaacbeb

                view.remove_item(item=button1)
                view.remove_item(item=button2)
                view.remove_item(item=button3)
                embed=discord.Embed(description=f'**[ Bet: 🪙 {"{:,}".format(bet)} ]** {resultText}', color=color)
                embed.set_author(name=f'{ctx.author.display_name} is playing Rock, Paper, Scissors', icon_url=ctx.author.display_avatar)
                embed.add_field(name=f'Dealer', value=f'{emoji[computerChoice]}', inline=True)
                embed.add_field(name=f'{ctx.author.display_name}', value=f'{emoji[playerChoice]}', inline=True)
                await msg.edit(embed=embed, view=view)

                updateCoins(userData, result, bet)