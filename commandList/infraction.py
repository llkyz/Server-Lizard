import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import asyncio
from datetime import datetime
from functions import *

def setup(client):
    @client.command() #!infraction
    async def infraction(ctx):
        if checkRoles(ctx.author, [423458739656458243, 407557898638589974]):
            profileChannel = client.get_channel(1035131570257932318)
            mylist = ctx.message.content.replace('!infraction ', '').split(' ')
            if mylist[0] == 'add':
                try:
                    user = await client.fetch_user(mylist[1])
                except:
                    await ctx.reply(embed=discord.Embed(title='Syntax Error', description='Please follow this format: `!infraction add [userID]` (e.g userID = 1032276665092538489)'))
                else:
                    view = discord.ui.View()
                    button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                    button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                    view.add_item(item=button1)
                    view.add_item(item=button2)
                    embed = discord.Embed(title=f'Adding infraction to user {mylist[1]} ({user})')
                    msg1 = await ctx.reply(embed=embed, view=view)

                    def check(m):
                        return m.message == msg1 and m.user == ctx.author
                    try:
                        interacted = await client.wait_for('interaction', timeout=300, check=check)
                    except asyncio.TimeoutError:
                        view.remove_item(item=button1)
                        view.remove_item(item=button2)
                        await msg1.edit(content='Timed out!', view=view)
                    else:
                        await interacted.response.defer()
                        view.remove_item(item=button1)
                        view.remove_item(item=button2)
                        await msg1.edit(view=view)
                        if interacted.data['custom_id'] == 'confirm':                    
                            embed = discord.Embed(title=f'Please enter details regarding the infraction below')
                            msg2 = await ctx.send(embed=embed)
                            
                            def checkMessage(m):
                                return m.channel == ctx.channel and m.author == ctx.author

                            try:
                                interacted = await client.wait_for('message', timeout=600, check=checkMessage)
                            except asyncio.TimeoutError:
                                await msg2.edit(content='Timed out!')
                            else:
                                newInfraction = interacted.content
                                embed = discord.Embed(title=f'Adding infraction to user {mylist[1]} ({user})')
                                embed.add_field(name='**Infraction**', value=f'> {newInfraction}')
                                view.add_item(item=button1)
                                view.add_item(item=button2)
                                msg3 = await ctx.send(embed=embed, view=view)
                                
                                def check2(m):
                                    return m.message == msg3 and m.user == ctx.author
                                try:
                                    interacted = await client.wait_for('interaction', timeout=300, check=check2)
                                except asyncio.TimeoutError:
                                    view.remove_item(item=button1)
                                    view.remove_item(item=button2)
                                    await msg3.edit(content='Timed out!', view=view)
                                else:
                                    await interacted.response.defer()
                                    view.remove_item(item=button1)
                                    view.remove_item(item=button2)
                                    await msg3.edit(view=view)
                                    if interacted.data['custom_id'] == 'confirm':
                                        found = 0
                                        async for message in profileChannel.history(limit=None): # change channel ID later
                                            if message.embeds and message.embeds[0].description and f'**User ID**: {user.id}' in message.embeds[0].description:
                                                found = 1
                                                embed = discord.Embed(title=message.embeds[0].title, description=message.embeds[0].description + '\n* ' + newInfraction + ' [' + timeConvert(datetime.utcnow()).strftime("%d %B %Y, %I:%M:%S%p") + ']')
                                                embed.set_thumbnail(url=user.display_avatar.url)
                                                await message.edit(embed=embed)
                                                embed = discord.Embed(title=f'Infraction added.', description=f'Link to updated profile: [\[Link\]]({message.jump_url})')
                                                await ctx.send(embed=embed)
                                                break
                                        if found == 0:
                                            embed = discord.Embed(title=f'Profile can\'t be found?! Contact your local lizard support')
                                            await ctx.send(embed=embed)
                                            
                                    elif interacted.data['custom_id'] == 'cancel':
                                        embed = discord.Embed(title=f'Infraction cancelled')
                                        await ctx.send(embed=embed)
                                        
                        elif interacted.data['custom_id'] == 'cancel':
                            embed = discord.Embed(title=f'Infraction cancelled')
                            await ctx.send(embed=embed)
                            
            elif mylist[0] == 'remove':
                try:
                    user = await client.fetch_user(mylist[1])
                except:
                    embed = discord.Embed(title='Syntax Error', description='Please follow this format: `!infraction remove [userID]` (e.g userID = 1032276665092538489)')
                    await ctx.reply(embed=embed)
                else:
                    embed = discord.Embed(title=f'Removing infraction from user {mylist[1]} ({user})')
                    view = discord.ui.View()
                    button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                    button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                    view.add_item(item=button1)
                    view.add_item(item=button2)
                    msg1 = await ctx.reply(embed=embed, view=view)

                    def check(m):
                        return m.message == msg1 and m.user == ctx.author
                    try:
                        interacted = await client.wait_for('interaction', timeout=300, check=check)
                    except asyncio.TimeoutError:
                        view.remove_item(item=button1)
                        view.remove_item(item=button2)
                        await msg1.edit(content='Timed out!', view=view)
                    else:
                        await interacted.response.defer()
                        view.remove_item(item=button1)
                        view.remove_item(item=button2)
                        await msg1.edit(view=view)
                        
                        if interacted.data['custom_id'] == 'cancel':
                            await ctx.send(embed=discord.Embed(title=f'Infraction removal cancelled'))
                            
                        elif interacted.data['custom_id'] == 'confirm':
                            found = 0
                            async for message in profileChannel.history(limit=None):
                                if message.embeds and message.embeds[0].description and f'**User ID**: {user.id}' in message.embeds[0].description:
                                    found = 1
                                    mystr = message.embeds[0].description.split('**Infractions**:')
                                    for x in range(len(mystr)):
                                        if mystr[x] == '':
                                            mystr.pop(x)
                                    if len(mystr) > 1:
                                        infractions = mystr[1].split('\n* ')
                                        embed = discord.Embed(title=f'Current infractions')
                                        infractions.pop(0)
                                        count = 1
                                        for x in infractions:
                                            embed.add_field(name=f'Infraction #{count}', value=f'> {x}', inline=False)
                                            count += 1
                                        await ctx.send(embed=embed)

                                        embed = discord.Embed(title=f'Please enter the # of the infraction you wish to remove')
                                        msg2 = await ctx.send(embed=embed)

                                        def checkMessage(m):
                                            return m.channel == ctx.channel and m.author == ctx.author
                                        try:
                                            interacted = await client.wait_for('message', timeout=600, check=checkMessage)
                                        except asyncio.TimeoutError:
                                            await msg2.edit(content='Timed out!')
                                        else:
                                            try:
                                                infractionNum = int(interacted.content) - 1
                                                if infractionNum < 0:
                                                    embed = discord.Embed(title=f'Invalid number entered. Please start over.')
                                                    await ctx.send(embed=embed)
                                                    break
                                                else:
                                                    embed = discord.Embed(title=f'Removing infraction', description=f'> {infractions[infractionNum]}')
                                                    view.add_item(item=button1)
                                                    view.add_item(item=button2)
                                                    msg3 = await ctx.send(embed=embed, view=view)

                                                    def check(m):
                                                        return m.message == msg3 and m.user == ctx.author
                                                    try:
                                                        interacted = await client.wait_for('interaction', timeout=300, check=check)
                                                    except asyncio.TimeoutError:
                                                        view.remove_item(item=button1)
                                                        view.remove_item(item=button2)
                                                        await msg3.edit(content='Timed out!', view=view)
                                                    else:
                                                        await interacted.response.defer()
                                                        view.remove_item(item=button1)
                                                        view.remove_item(item=button2)
                                                        await msg3.edit(view=view)
                                                        
                                                        if interacted.data['custom_id'] == 'cancel':
                                                            await ctx.send(embed=discord.Embed(title=f'Infraction removal cancelled'))
                                                            break
                                                        
                                                        elif interacted.data['custom_id'] == 'confirm':
                                                            infractions.pop(infractionNum)
                                                            revisedInfractions = ""
                                                            for x in infractions:
                                                                revisedInfractions += "\n* "
                                                                revisedInfractions += x
                                                            embed = discord.Embed(title=message.embeds[0].title, description=mystr[0] + '**Infractions**:' + revisedInfractions)
                                                            embed.set_thumbnail(url=user.display_avatar.url)
                                                            await message.edit(embed=embed)
                                                            embed = discord.Embed(title=f'Infraction removed.', description=f'Link to updated profile: [\[Link\]]({message.jump_url})')
                                                            await ctx.send(embed=embed)
                                                            break

                                            except:
                                                await ctx.send(embed=discord.Embed(title=f'Invalid number entered'))
                                                break
                                            
                                    else:
                                        await ctx.send(embed=discord.Embed(title=f'This user has no infractions'))
                                        break
                                
                            if found == 0:
                                embed = discord.Embed(title=f'Profile can\'t be found?! Contact your local lizard support')
                                await ctx.send(embed=embed)
                            
            else:
                await ctx.reply(embed=discord.Embed(title='Syntax Error', description='Please use `!infraction add [userID]` or `!infraction remove [userID]` (e.g userID = 1032276665092538489)'))
