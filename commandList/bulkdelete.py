import discord
from discord.ext import commands
import asyncio
from discord import Button, ButtonStyle
from datetime import timedelta
import math
from functions import *

docs = {

    "aliases":[],

    "usage":"!bulkdelete",

    "description":"Allows you to select and delete a range of messages from any channel.\nCAUTION: Messages will be permanently deleted and cannot be retrieved.",

    "category":"admin-messages"
    
    }

def setup(client):
    @client.command()
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)  
    async def bulkdelete(ctx):
        try:
            await ctx.message.delete()
        except:
            await ctx.author.send(f'Please use this command in a server channel.')
        else:
            if hasAdminRole(ctx) or checkOwner(ctx):
                view = discord.ui.View()
                button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                view.add_item(item=button1)
                view.add_item(item=button2)
                embed = discord.Embed(title=f'__**You are attempting to bulk delete a section of messages**__', description=f'Do you wish to proceed?', color=0xFF5733)
                mymsg = await ctx.author.send(embed=embed, view=view)

                def checkButton(m):
                    return m.message == mymsg and m.user == ctx.author

                try:
                    interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                except asyncio.TimeoutError:
                    view.clear_items()
                    await mymsg.edit(content='Timed out!', view=view)
                else:
                    await interacted.response.defer()
                    view.clear_items()
                    await mymsg.edit(view=view)

                    if interacted.data['custom_id'] == 'cancel':
                        embed=discord.Embed(title=f'Bulk delete cancelled', color=0xFF5733)
                        await ctx.author.send(embed=embed)

                    elif interacted.data['custom_id'] == 'confirm':
                        embed = discord.Embed(title=f'Please enter the URL link to the first message to start from', description=f'example: <https://discord.com/channels/123456789012345678/1234567890123456789/1234567890123456789>', color=0xFF5733)
                        msg2 = await ctx.author.send(embed=embed)

                        def check(m):
                            return "http" in m.content and m.channel.type is discord.ChannelType.private and m.author == ctx.author

                        checkFirstMessage = 0
                        while (checkFirstMessage == 0):
                            try:
                                msg3 = await client.wait_for('message', timeout=300, check=check)
                            except asyncio.TimeoutError:
                                await ctx.author.send(embed=discord.Embed(title="Timed out!"))
                                checkFirstMessage = 2
                            else:
                                try:
                                    getLink = msg3.content.replace("https://discord.com/channels/","")
                                    idList = getLink.split("/")
                                    myChannel = client.get_channel(int(idList[1]))
                                    fetched = await myChannel.fetch_message(int(idList[2]))
                                except:
                                    await ctx.author.send(embed=discord.Embed(title="Error, could not retrieve message. Please try again"))
                                else:
                                    checkFirstMessage = 1

                        if checkFirstMessage == 1:
                            embed=discord.Embed(title=f"Bulk Delete [Start]", description="**Server**: " + str(fetched.guild) + "\n**Channel**: #" + str(fetched.channel) + "\n**Author**: " + str(fetched.author) + "\n**Time**: " + timeConvertShort(fetched.created_at), color=0xFF5733)
                            embed.add_field(name="Message Link", value=f"> [\[Link\]]({fetched.jump_url})", inline=False)
                            embed.add_field(name="Message Content", value=f"> {fetched.content}", inline=False)
                            await ctx.author.send(embed=embed)
                            embed=discord.Embed(title=f'Please enter the URL link to the last message to end at', description=f'example: <https://discord.com/channels/123456789012345678/1234567890123456789/1234567890123456789>', color=0xFF5733)
                            msg4 = await ctx.author.send(embed=embed)

                            checkSecondMessage = 0
                            while (checkSecondMessage == 0):
                                try:
                                    msg5 = await client.wait_for('message', timeout=300, check=check)
                                except asyncio.TimeoutError:
                                    await ctx.author.send(embed=discord.Embed(title="Timed out!"))
                                    checkSecondMessage = 2
                                else:
                                    try:
                                        getLink = msg5.content.replace("https://discord.com/channels/","")
                                        idList = getLink.split("/")
                                        myChannel = client.get_channel(int(idList[1]))
                                        fetched2 = await myChannel.fetch_message(idList[2])
                                    except:
                                        await ctx.author.send(embed=discord.Embed(title="Error, could not retrieve message. Please try again"))
                                    else:
                                        if fetched2.channel.id != fetched.channel.id:
                                            await ctx.author.send(embed=discord.Embed(title="Error, this message belongs to a different channel. Please try again"))
                                        else:
                                            checkSecondMessage = 1

                        if checkFirstMessage == 1 and checkSecondMessage == 1:
                            embed=discord.Embed(title=f"Bulk Delete [End]", description="**Server**: " + str(fetched2.guild) + "\n**Channel**: #" + str(fetched2.channel) + "\n**Author**: " + str(fetched2.author) + "\n**Time**: " + timeConvertShort(fetched2.created_at), color=0xFF5733)
                            embed.add_field(name="Message Link", value=f"> [\[Link\]]({fetched2.jump_url})", inline=False)
                            embed.add_field(name="Message Content", value=f"> {fetched2.content}", inline=False)
                            await ctx.author.send(embed=embed)
                            
                            msg6 = await ctx.author.send(embed=discord.Embed(title=f"Calculating...", color=0xFF5733))

                            if fetched.created_at < fetched2.created_at:
                                dateStart = fetched.created_at - timedelta(seconds=0.1)
                                dateEnd = fetched2.created_at + timedelta(seconds=0.1)
                            else:
                                dateStart = fetched2.created_at - timedelta(seconds=0.1)
                                dateEnd = fetched.created_at + timedelta(seconds=0.1)

                            messageArray = []
                            messagePreview = ""
                            async for x in fetched.channel.history(limit=3000, before=dateEnd, after=dateStart):
                                if len(x.content) > 27:
                                    shortMessage = x.content[:27] + ".."
                                else:
                                    shortMessage = x.content
                                messageArray.append({'message': shortMessage, 'time': timeConvertShort(x.created_at)})

                            currentPage = 1

                            if (len(messageArray) < 20):
                                maxPage = 1
                                pageLength = len(messageArray)
                            else:
                                pageLength = 20
                                if (len(messageArray) % 20 == 0):
                                    maxPage = len(messageArray) / 20
                                else:
                                    maxPage = math.ceil((len(messageArray) / 20))

                            for x in range(pageLength):
                                messagePreview += "> "+ messageArray[x]['time'] + "| " + messageArray[x]['message'] + "\n"

                            view.add_item(item=button1)
                            view.add_item(item=button2)
                            embedArray=discord.Embed(title=f"Delete {len(messageArray)} messages?", description="(Search Limit: Up to 3000 messages from everyone since the start date)\n\n**Server**: " + str(fetched.guild) + "\n**Channel**: #" + str(fetched.channel), color=0xFF5733)
                            embedArray.add_field(name="Date", value=f"> **Start**: " + timeConvertShort(dateStart) + "\n> **End**: " + timeConvertShort(dateEnd), inline=False)
                            embedArray.add_field(name=f"Message Preview (page {currentPage} of {maxPage})", value=messagePreview, inline=False)
                            await msg6.edit(embed=embedArray, view=view)
                            await msg6.add_reaction('⬅')
                            await msg6.add_reaction('➡')

                            def checkButton2(m):
                                return m.message == msg6 and m.user == ctx.author

                            def checkReaction(m,user):
                                return m.message == msg6 and user == ctx.author and (m.emoji == '⬅' or m.emoji == '➡')

                            exitLoop = 0
                            while (exitLoop == 0):
                                done, pending = await asyncio.wait([
                                    client.loop.create_task(client.wait_for('interaction', check=checkButton2)),
                                    client.loop.create_task(client.wait_for('reaction_add', check=checkReaction)),
                                    client.loop.create_task(client.wait_for('reaction_remove', check=checkReaction)),
                                    ], timeout=300, return_when=asyncio.FIRST_COMPLETED)
                                try:
                                    myResult = done.pop().result()
                                except:
                                    view.clear_items()
                                    await msg6.edit(content='Timed out!', view=view)
                                    exitLoop = 1
                                else:        
                                    if type(myResult) is discord.interactions.Interaction:
                                        await myResult.response.defer()
                                        view.clear_items()
                                        await msg6.edit(view=view)
                                        
                                        if myResult.data['custom_id'] == 'confirm':
                                            embed=discord.Embed(title=f'Processing...', color=0xFF5733)
                                            progress = await ctx.author.send(embed=embed)
                                            deleted = await fetched.channel.purge(limit=3000, before=dateEnd, after=dateStart)
                                            embed=discord.Embed(title=f'{len(deleted)} messages deleted from #{fetched.channel} in {fetched.guild}', color=0x00FF00)
                                            await progress.edit(embed=embed)
                                            await fetched.channel.send(f'Deleted {len(deleted)} message(s).')
                                        elif myResult.data['custom_id'] == 'cancel':
                                            embed=discord.Embed(title=f'Bulk delete cancelled', color=0xFF5733)
                                            await ctx.author.send(embed=embed)
                                        exitLoop = 1
                                            
                                    elif type(myResult) is tuple:
                                        if myResult[0].emoji == '⬅':
                                            currentPage -= 1
                                            if currentPage < 1:
                                                currentPage = maxPage
                                                
                                        elif myResult[0].emoji == '➡':
                                            currentPage += 1
                                            if currentPage > maxPage:
                                                currentPage = 1
                                                
                                        messagePreview = ""

                                        startIndex = (currentPage - 1) * 20
                                        if currentPage == maxPage:
                                            endIndex = len(messageArray)
                                        else:
                                            endIndex = currentPage * 20
                                        
                                        for x in range(startIndex, endIndex):
                                            messagePreview += "> "+ messageArray[x]['time'] + "| " + messageArray[x]['message'] + "\n"

                                        embed_dict = embedArray.to_dict()
                                        for field in embed_dict["fields"]:
                                            if "Message Preview" in field["name"]:
                                                field["name"] = f"Message Preview (page {currentPage} of {maxPage})"
                                                field["value"] = messagePreview

                                        embed = discord.Embed.from_dict(embed_dict)
                                        await msg6.edit(embed=embed)
