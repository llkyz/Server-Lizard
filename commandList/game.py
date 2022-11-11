import discord
from discord.ext import commands
import random
from discord import Button, ButtonStyle

def setup(client):
    @client.command() #!game
    async def game(ctx):
        channel = ctx.channel

        view = discord.ui.View()
        button1 = discord.ui.Button(label="Scissors ✂", style=ButtonStyle.grey, custom_id='scissors')
        button2 = discord.ui.Button(label="Paper 📰", style=ButtonStyle.grey, custom_id='paper')
        button3 = discord.ui.Button(label="Stone 🗿", style=ButtonStyle.grey, custom_id='stone')
        view.add_item(item=button1)
        view.add_item(item=button2)
        view.add_item(item=button3)
        embed=discord.Embed(title=f'Pick your choice!', color=0xaacbeb)
        msg = await ctx.reply(embed=embed, view=view)

        def check(m):
            return m.message == msg and m.user == ctx.author

        try:
            interacted = await client.wait_for('interaction', timeout=60, check=check)
        except asyncio.TimeoutError:
            button1.disabled = True
            button2.disabled = True
            button3.disabled = True
            await msg.edit(content='Timed out!', view=view)
        else:
            await interacted.response.defer()
            button1.disabled = True
            button2.disabled = True
            button3.disabled = True
            await msg.edit(view=view)

            choices = ['Scissors', 'Paper', 'Stone']
            
            if interacted.data['custom_id'] == 'scissors':
                playerChoice = 0
            elif interacted.data['custom_id'] == 'paper':
                playerChoice = 1
            elif interacted.data['custom_id'] == 'stone':
                playerChoice = 2
                
            computerChoice = random.randint(0,2)
            
            if (playerChoice == computerChoice):
                title = 'It\'s a tie!'
                color = 0xaacbeb
                text = f'Both of us chose {choices[playerChoice]}!'
            else:
                text = f'You chose {choices[playerChoice]} and I chose {choices[computerChoice]}!'
                if (playerChoice == 0):
                    if (computerChoice == 1):
                        title = 'You win!'
                        color = 0x00FF00
                    else:
                        title = 'I win!'
                        color = 0xFF5733
                elif (playerChoice == 1):
                    if (computerChoice == 0):
                        title = 'I win!'
                        color = 0xFF5733
                    else:
                        title = 'You win!'
                        color = 0x00FF00
                else:
                    if (computerChoice == 0):
                        title = 'You win!'
                        color = 0x00FF00
                    else:
                        title = 'I win!'
                        color = 0xFF5733
                    
            await channel.send(embed=discord.Embed(title=title,description=text, color=color))
