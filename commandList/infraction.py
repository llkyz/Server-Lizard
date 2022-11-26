import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import asyncio
from functions import *
from datetime import datetime

docs = {

    "aliases":['infractions'],

    "usage":"!infraction [userID], !infraction [@user]",

    "description":"View, add, or remove an infraction on a user's profile entry for record-keeping purposes.\n\nThis requires user profiles (`!userprofiles set` / `!userprofiles populate`) to be enabled and generated.",

    "category":"admin-disciplinary"
    
    }

def setup(client):
    @client.command(aliases=['infractions'])
    async def infraction(ctx):
        if hasAdminRole(ctx) or checkOwner(ctx):
            sqlCursor.execute('SELECT userProfilesChannel FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
            channelData = sqlCursor.fetchone()

            if channelData == None:
                await ctx.reply("A User Profile channel has not been set yet. Please set one up using `!userprofiles` and generate the profiles first.")
            else:
                profileChannel = client.get_channel(channelData[0])
                userId = ctx.message.content.split(' ')[1].replace("<@","").replace(">","")
                try:
                    user = await client.fetch_user(userId)
                except:
                    await ctx.reply(embed=discord.Embed(title='Syntax Error', description='Please follow this format: `!infraction [@user]` or `!infraction [userID]` (e.g userID = 1032276665092538489)'), delete_after=60)
                else:
                    targetMessage = ""
                    async for message in profileChannel.history(limit=None):
                        if message.embeds and message.embeds[0].description and f'**User ID**: {user.id}' in message.embeds[0].description:
                            targetMessage = message
                            embed = discord.Embed(title=message.embeds[0].title, description=message.embeds[0].description)
                            embed.set_thumbnail(url=user.display_avatar.url)
                            break
                    if targetMessage == "":
                        embed = discord.Embed(title=f'Profile can\'t be found?! Contact your local lizard support')
                        await ctx.send(embed=embed)
                    else:
                        infractionStart = targetMessage.embeds[0].description.index('**Infractions**:') + 16
                        infractions = message.embeds[0].description[infractionStart:]
                        infractionList = infractions.split('\n* ')
                        infractionList.pop(0)

                        view = discord.ui.View()
                        button1 = discord.ui.Button(label="Add", style=ButtonStyle.green, custom_id='add')
                        button2 = discord.ui.Button(label="Remove", style=ButtonStyle.red, custom_id='remove')
                        button3 = discord.ui.Button(label="Done", style=ButtonStyle.gray, custom_id='done')
                        view.add_item(item=button1)
                        if len(infractionList) != 0:
                            view.add_item(item=button2)
                        view.add_item(item=button3)
                        msg1 = await ctx.reply(content="**Viewing Infractions**", embed=embed, view=view)

                        def checkButton(m):
                            return m.message == msg1 and m.user == ctx.author
                        try:
                            interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                        except asyncio.TimeoutError:
                            await msg1.edit(content='Timed out!', view=None)
                        else:
                            await interacted.response.defer()
                            await msg1.edit(view=None)
                            
                            if interacted.data['custom_id'] == 'done':
                                return
                            elif interacted.data['custom_id'] == 'add':
                                msg2 = await ctx.send(embed=discord.Embed(title="Please enter details regarding the infraction below"))

                                def checkMessage(m):
                                    return m.channel == ctx.channel and m.author == ctx.author

                                try:
                                    interacted = await client.wait_for('message', timeout=600, check=checkMessage)
                                except asyncio.TimeoutError:
                                    await msg2.edit(content='Timed out!')
                                else:
                                    newInfraction = interacted.content
                                    infractionStart = targetMessage.embeds[0].description.index('**Infractions**:') + 16

                                    embed = discord.Embed(title=targetMessage.embeds[0].title, description=targetMessage.embeds[0].description[:infractionStart] + f'\n* {newInfraction} [{timeConvertShort(datetime.utcnow())}]' + targetMessage.embeds[0].description[infractionStart:])
                                    embed.set_thumbnail(url=user.display_avatar.url)
                                    edited = await targetMessage.edit(embed=embed)

                                    embed = discord.Embed(title=edited.embeds[0].title, description=edited.embeds[0].description)
                                    embed.set_thumbnail(url=user.display_avatar.url)
                                    await ctx.send(embed=embed)

                            elif interacted.data['custom_id'] == 'remove':
                                def makeOptions(myList):
                                    return discord.SelectOption(label=f'Infraction #{myList[0]}', value=f'{myList[0]}', description=f'{myList[1]}')

                                options = list(map(makeOptions, list(enumerate(infractionList, start=1))))
                                options.append(discord.SelectOption(label=f'Cancel', value=f'0'))
                                view = discord.ui.View()
                                myMenu = discord.ui.Select(placeholder="Choose an infraction to remove", options=options)
                                view.add_item(myMenu)

                                msg1 = await ctx.send(view=view)

                                def checkButton(m):
                                    return m.message == msg1 and m.user == ctx.author
                                try:
                                    interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                                except asyncio.TimeoutError:
                                    await msg1.edit(content='Timed out!', view=None)
                                else:
                                    await interacted.response.defer()
                                    optionSelected = interacted.data["values"][0]
                                    await msg1.delete()

                                    if optionSelected == '0':
                                        await ctx.send(embed=discord.Embed(title=f'Infraction removal cancelled'))
                                    else:
                                        infractionList.pop(int(optionSelected)-1)
                                        revisedInfractionList = ""
                                        for x in infractionList:
                                            revisedInfractionList += "\n* "
                                            revisedInfractionList += x
                                        embed = discord.Embed(title=targetMessage.embeds[0].title, description=targetMessage.embeds[0].description[:infractionStart] + revisedInfractionList)
                                        embed.set_thumbnail(url=user.display_avatar.url)
                                        edited = await targetMessage.edit(embed=embed)
                                        embed = discord.Embed(title=edited.embeds[0].title, description=edited.embeds[0].description)
                                        embed.set_thumbnail(url=user.display_avatar.url)
                                        await ctx.send(content=f'**Removed Infraction #{optionSelected}**', embed=embed)
        else:
            await ctx.send(embed=discord.Embed(title=f'You do not have permission to use that command'), delete_after=20)