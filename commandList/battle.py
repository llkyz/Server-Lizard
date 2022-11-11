import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import asyncio

def setup(client):
    @client.command() #!battle
    async def battle(ctx):
        try:
            getOpponentId = ctx.message.content.replace('!battle <@','')
            getOpponentId = int(getOpponentId.replace('>',''))
            guild = await client.fetch_guild(ctx.guild.id)
            getUser = await guild.fetch_member(getOpponentId)
            if ctx.guild.get_member(getOpponentId) is None:
                await ctx.reply('Invalid syntax! Please use `!battle {@user}`')
            else:
                if getUser.id == 1032276665092538489:
                    await ctx.reply('Use !game to battle me!')
                elif getUser == ctx.author:
                    await ctx.reply('You cannot battle yourself!')
                else:
                    channel = ctx.channel
                    view = discord.ui.View()
                    button1 = discord.ui.Button(label="Accept", style=ButtonStyle.green, custom_id='accept')
                    button2 = discord.ui.Button(label="Decline", style=ButtonStyle.red, custom_id='decline')
                    view.add_item(item=button1)
                    view.add_item(item=button2)
                    mymsg = await ctx.reply(content=f'{getUser.mention}, {ctx.author.display_name} wants to battle! ✂📰🗿', view=view)

                    def checkButton(m):
                        return m.message == mymsg and m.user.id == getOpponentId

                    try:
                        interacted = await client.wait_for('interaction', timeout=120, check=checkButton)
                    except asyncio.TimeoutError:
                        button1.disabled = True
                        button2.disabled = True
                        await mymsg.edit(content='Timed out!', view=view)
                    else:
                        if interacted.data['custom_id'] == 'accept':
                            await interacted.response.defer()
                            button1.disabled = True
                            button2.disabled = True
                            await mymsg.edit(view=view)
                            button1 = discord.ui.Button(label="Scissors ✂", style=ButtonStyle.grey, custom_id='scissors')
                            button2 = discord.ui.Button(label="Paper 📰", style=ButtonStyle.grey, custom_id='paper')
                            button3 = discord.ui.Button(label="Stone 🗿", style=ButtonStyle.grey, custom_id='stone')
                            view.clear_items()
                            view.add_item(item=button1)
                            view.add_item(item=button2)
                            view.add_item(item=button3)
                            embed = discord.Embed(title='**Battle Commencing!**', description=f'Waiting for players to pick:',color=0x00FF00)
                            embed.add_field(name="Player 1", value=f'> {ctx.author.display_name}', inline=True)
                            embed.add_field(name="Player 2", value=f'> {getUser.nick}', inline=True)
                            msg2 = await ctx.channel.send(embed=embed, view=view)

                            def checkPlayer(m):
                                return m.message == msg2 and (m.user == ctx.author or m.user == getUser)

                            def checkPlayer2(m):
                                return m.message == msg2 and m.user == remainingPlayer

                            try:
                                interacted = await client.wait_for('interaction', timeout=120, check=checkPlayer)
                            except asyncio.TimeoutError:
                                button1.disabled = True
                                button2.disabled = True
                                button3.disabled = True
                                await msg2.edit(content='Timed out!', view=view)
                            else:
                                await interacted.response.defer()
                                if interacted.user == ctx.author:
                                    remainingPlayer = getUser
                                    if interacted.data['custom_id'] == 'scissors':
                                        player1Choice = 0
                                    elif interacted.data['custom_id'] == 'paper':
                                        player1Choice = 1
                                    elif interacted.data['custom_id'] == 'stone':
                                        player1Choice = 2
                                    embed.set_field_at(index=0, name="Player 1", value=f'> {ctx.author.display_name} ✅', inline=True)
                                elif interacted.user == getUser:
                                    remainingPlayer = ctx.author
                                    if interacted.data['custom_id'] == 'scissors':
                                        player2Choice = 0
                                    elif interacted.data['custom_id'] == 'paper':
                                        player2Choice = 1
                                    elif interacted.data['custom_id'] == 'stone':
                                        player2Choice = 2
                                    embed.set_field_at(index=1, name="Player 2", value=f'> {getUser.nick} ✅', inline=True)
                                await msg2.edit(embed=embed)

                                try:
                                    interacted = await client.wait_for('interaction', timeout=120, check=checkPlayer2)
                                except asyncio.TimeoutError:
                                    button1.disabled = True
                                    button2.disabled = True
                                    button3.disabled = True
                                    await msg2.edit(content='Timed out!', view=view)
                                else:
                                    await interacted.response.defer()

                                    button1.disabled = True
                                    button2.disabled = True
                                    button3.disabled = True
                                    await msg2.edit(view=view)
                                    
                                    if interacted.user == getUser:
                                        if interacted.data['custom_id'] == 'scissors':
                                            player2Choice = 0
                                        elif interacted.data['custom_id'] == 'paper':
                                            player2Choice = 1
                                        elif interacted.data['custom_id'] == 'stone':
                                            player2Choice = 2
                                        embed.set_field_at(index=1, name="Player 2", value=f'> {getUser.nick} ✅', inline=True)
                                    elif interacted.user == ctx.author:
                                        if interacted.data['custom_id'] == 'scissors':
                                            player1Choice = 0
                                        elif interacted.data['custom_id'] == 'paper':
                                            player1Choice = 1
                                        elif interacted.data['custom_id'] == 'stone':
                                            player1Choice = 2
                                        embed.set_field_at(index=0, name="Player 1", value=f'> {ctx.author.display_name} ✅', inline=True)
                                    await msg2.edit(embed=embed)

                                    choices = ['Scissors', 'Paper', 'Stone']
                                    if (player1Choice == player2Choice):
                                        title = 'It\'s a tie!'
                                        text = f'Both players chose {choices[player1Choice]}!'
                                    else:
                                        text = f'{ctx.author.display_name} chose {choices[player1Choice]} and {getUser.nick} chose {choices[player2Choice]}!'
                                        if (player1Choice == 0):
                                            if (player2Choice == 1):
                                                title = f'{ctx.author.display_name} wins!'
                                            else:
                                                title = f'{getUser.nick} wins!'
                                        elif (player1Choice == 1):
                                            if (player2Choice == 0):
                                                title = f'{getUser.nick} wins!'
                                            else:
                                                title = f'{ctx.author.display_name} wins!'
                                        else:
                                            if (player2Choice == 0):
                                                title = f'{ctx.author.display_name} wins!'
                                            else:
                                                title = f'{getUser.nick} wins!'

                                    await channel.send(embed=discord.Embed(title=title,description=text, color=0x00FF00))
                        else:
                            await interacted.response.defer()
                            button1.disabled = True
                            button2.disabled = True
                            await mymsg.edit(view=view)
                            await mymsg.reply(content='Battle declined.')
        except:
            await ctx.reply('Invalid syntax! Please use `!battle {@user}`')
