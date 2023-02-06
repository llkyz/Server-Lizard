import discord
from discord.ext import commands
from functions import *
import asyncio
from discord import Button, ButtonStyle
import math
from copy import deepcopy

docs = {

    "aliases":[],

    "usage":"!embed create, !embed edit [msg id], !embed delete [msg id]",

    "description":"Create an embedded message using my embed builder and send it to a specific channel. The embed builder interface will be sent through your DMs.\n\nRequires embed role permission to use. Please contact a server admin if you require this permission.",

    "category":"utility"
    
    }

def setup(client):
    @client.command()
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
    async def embed(ctx, arg=None, arg2=None):
        if hasEmbedRole(ctx) or hasAdminRole(ctx) or checkOwner(ctx):

            if arg == None and arg2 == None:
                await ctx.reply("Please use the following format: `!embed create` / `!embed edit [msg id]` / `!embed delete [msg id]`", delete_after=20)
            elif arg.lower() == "create" or arg.lower() == "edit":

                if arg.lower() == "edit":
                    try:
                        fetchedMessage = await ctx.channel.fetch_message(arg2)
                    except:
                        await ctx.reply("Message not found. Please ensure that you're entering this command in the channel that the message is in, and use the following format: !embed edit [msg id]. The message ID can be found in the embed's footer")
                        return
                    else:
                        embed_dict = fetchedMessage.embeds[0].to_dict()

                        if f'Message ID: {fetchedMessage.id}' in embed_dict["footer"]["text"] and fetchedMessage.author.id == 1032276665092538489:
                            pass
                        else:
                            await ctx.reply("That message is not a custom embedded message created by Server Lizard.")
                            return
                    
                elif arg.lower() == "create":
                    embed_dict = {'title': f'This is your new embed message!', 'footer': {'text': f'created by {ctx.author.display_name} | Message ID: <message ID will be entered here>'}}

                section = "overall"
                sectionValue = ""
                valueType = ""
                currentField = None
                controllerText = f'Creating new embed in `#{ctx.channel.name}` on {ctx.guild.name}'
                view = discord.ui.View()

                def addSection():
                    if section == "image":
                        embed_dict["image"] = {'url': 'https://images.emojiterra.com/twitter/v13.1/512px/1f98e.png'}
                    elif section == "thumbnail":
                        embed_dict["thumbnail"] = {'url': 'https://images.emojiterra.com/twitter/v13.1/512px/1f98e.png'}
                    elif section == "author":
                        embed_dict["author"] = {'name': 'Server Lizard', 'url': 'https://discord.com/assets/1703f9a3721beece0d66f10c0ef9d3d0.svg', 'icon_url': 'https://images.emojiterra.com/twitter/v13.1/512px/1f98e.png'}

                def deleteSection():
                    embed_dict.pop(section)

                def addField():
                    if 'fields' not in embed_dict:
                        embed_dict["fields"] = []
                    if len(embed_dict["fields"]) < 15:
                        x = len(embed_dict["fields"]) + 1
                        embed_dict["fields"].append({'name': f'Field {x}', 'value': 'Field Value', 'inline': False})
                        return True
                    else:
                        return False

                def editValue(content, limit=None):
                    if section == "fieldmenu":
                        if content.replace(" ","") == "":
                            controllerText = f'Navigating [{section}] -> [field {currentField + 1}] -> [{sectionValue}]\n\nValue cannot be blank.'
                        elif len(content) > limit:
                            controllerText = f'Navigating [{section}] -> [field {currentField + 1}] -> [{sectionValue}]\n\nExceeded limit of {limit} characters. You entered {len(content)} characters.'
                        else:
                            embed_dict['fields'][currentField][sectionValue] = content
                            controllerText = f'Navigating [{section}] -> [field {currentField + 1}] -> [{sectionValue}]\n\n[{sectionValue}] edited.'

                    elif (sectionValue == 'url' or sectionValue == 'icon_url') and content[:7].lower() != 'http://' and content[:8].lower() != 'https://':
                        controllerText = f'Navigating [{section}] -> [{sectionValue}]\n\nInvalid input. You need to enter a **http** or **https** link.'

                    elif sectionValue == 'color':
                        embed_dict[sectionValue] = content
                        controllerText = f'Navigating [{section}] -> [{sectionValue}]\n\n[{sectionValue}] added/edited.'
                    
                    else:
                        if len(content) > limit:
                            controllerText = f'Navigating [{section}] -> [{sectionValue}]\n\nExceeded limit of {limit} characters.'
                        else:
                            if section == "main":
                                embed_dict[sectionValue] = content
                            else:
                                embed_dict[section][sectionValue] = content
                            controllerText = f'Navigating [{section}] -> [{sectionValue}]\n\n[{sectionValue}] added/edited.'
                    return controllerText

                def deleteValue():
                    if section == "main":
                        embed_dict.pop(sectionValue)
                    else:
                        embed_dict[section].pop(sectionValue)

                def overallView(myList):
                    myList.append(discord.ui.Button(label="Main Body", style=ButtonStyle.grey, row=0, custom_id='section main'))
                    myList.append(discord.ui.Button(label="Fields", style=ButtonStyle.grey, row=0, custom_id='section fieldmenu'))
                    myList.append(discord.ui.Button(label="Author", style=ButtonStyle.grey, row=1, custom_id='section author'))
                    myList.append(discord.ui.Button(label="Image", style=ButtonStyle.grey, row=1, custom_id='section image'))
                    myList.append(discord.ui.Button(label="Thumbnail", style=ButtonStyle.grey, row=1, custom_id='section thumbnail'))
                    myList.append(discord.ui.Button(label="Create Embed", style=ButtonStyle.green, row=4, custom_id='execute create'))
                    myList.append(discord.ui.Button(label="Cancel", style=ButtonStyle.red, row=4, custom_id='execute cancel'))
                    return myList

                def mainView(myList):
                    myList.append(discord.ui.Button(label="Title", style=ButtonStyle.grey, row=0, custom_id='value title regular'))
                    myList.append(discord.ui.Button(label="Description", style=ButtonStyle.grey, row=0, custom_id='value description regular'))
                    myList.append(discord.ui.Button(label="Color", style=ButtonStyle.grey, row=0, custom_id='value color regular'))
                    myList.append(discord.ui.Button(label="Back", style=ButtonStyle.blurple, row=4, custom_id='section overall'))
                    return myList

                def fieldMenuView(myList):
                    if 'fields' in embed_dict:
                        for x in range(len(embed_dict["fields"])):
                            myList.append(discord.ui.Button(label=f'Field {x+1}', style=ButtonStyle.grey, row=math.floor(x/5), custom_id=f'section field {x}'))
                    myList.append(discord.ui.Button(label="Add New Field", style=ButtonStyle.blurple, row=3, custom_id='field add'))
                    myList.append(discord.ui.Button(label="Back", style=ButtonStyle.blurple, row=4, custom_id='section overall'))
                    return myList

                def fieldView(myList):
                    myList.append(discord.ui.Button(label="Name", style=ButtonStyle.grey, row=0, custom_id='value name perm'))
                    myList.append(discord.ui.Button(label="Value", style=ButtonStyle.grey, row=0, custom_id='value value perm'))
                    myList.append(discord.ui.Button(label="Inline", style=ButtonStyle.grey, row=0, custom_id='value inline'))
                    myList.append(discord.ui.Button(label="Delete Field", style=ButtonStyle.red, row=4, custom_id='field remove'))
                    myList.append(discord.ui.Button(label="Back", style=ButtonStyle.blurple, row=4, custom_id='section fieldmenu'))
                    return myList

                def authorView(myList):
                    if 'author' in embed_dict:
                        myList.append(discord.ui.Button(label="Name", style=ButtonStyle.grey, row=0, custom_id='value name regular'))
                        myList.append(discord.ui.Button(label="URL", style=ButtonStyle.grey, row=0, custom_id='value url regular'))
                        myList.append(discord.ui.Button(label="Icon URL", style=ButtonStyle.grey, row=0, custom_id='value icon_url regular'))
                        myList.append(discord.ui.Button(label="Delete Section", style=ButtonStyle.red, row=3, custom_id='execute section remove'))
                    else:
                        myList.append(discord.ui.Button(label="Create Section", style=ButtonStyle.blurple, row=0, custom_id='execute section add'))
                    myList.append(discord.ui.Button(label="Back", style=ButtonStyle.blurple, row=4, custom_id='section overall'))
                    return myList

                def imageView(myList):
                    if 'image' in embed_dict:
                        myList.append(discord.ui.Button(label="URL", style=ButtonStyle.grey, row=0, custom_id='value url perm'))
                        myList.append(discord.ui.Button(label="Delete Section", style=ButtonStyle.red, row=3, custom_id='execute section remove'))
                    else:
                        myList.append(discord.ui.Button(label="Create Section", style=ButtonStyle.blurple, row=0, custom_id='execute section add'))
                    myList.append(discord.ui.Button(label="Back", style=ButtonStyle.blurple, row=4, custom_id='section overall'))
                    return myList

                def thumbnailView(myList):
                    if 'thumbnail' in embed_dict:
                        myList.append(discord.ui.Button(label="URL", style=ButtonStyle.grey, row=0, custom_id='value url perm'))
                        myList.append(discord.ui.Button(label="Delete Section", style=ButtonStyle.red, row=3, custom_id='execute section remove'))
                    else:
                        myList.append(discord.ui.Button(label="Create Section", style=ButtonStyle.blurple, row=0, custom_id='execute section add'))
                    myList.append(discord.ui.Button(label="Back", style=ButtonStyle.blurple, row=4, custom_id='section overall'))
                    return myList

                def valueView(myList):
                    myList.append(discord.ui.Button(label="Add / Edit", style=ButtonStyle.grey, row=0, custom_id='execute add'))
                    if section != "main" and sectionValue in embed_dict[section]:
                        myList.append(discord.ui.Button(label="Remove", style=ButtonStyle.red, row=0, custom_id='execute remove'))
                    elif section == "main" and sectionValue in embed_dict:
                        myList.append(discord.ui.Button(label="Remove", style=ButtonStyle.red, row=0, custom_id='execute remove'))
                    myList.append(discord.ui.Button(label="Back", style=ButtonStyle.blurple, row=4, custom_id=f'section {section}'))
                    return myList

                def valuePermView(myList):
                    myList.append(discord.ui.Button(label="Edit", style=ButtonStyle.grey, row=0, custom_id='execute add'))
                    myList.append(discord.ui.Button(label="Back", style=ButtonStyle.blurple, row=4, custom_id=f'section {section}'))
                    return myList

                def inlineView(myList):
                    myList.append(discord.ui.Button(label="True", style=ButtonStyle.grey, row=0, custom_id='inline true'))
                    myList.append(discord.ui.Button(label="False", style=ButtonStyle.grey, row=0, custom_id='inline false'))
                    myList.append(discord.ui.Button(label="Back", style=ButtonStyle.blurple, row=4, custom_id=f'section {section}'))
                    return myList

                def createView(viewType):
                    view = discord.ui.View()
                    buttonList = []
                    buttonList = viewType(buttonList)
                    for x in buttonList:
                        view.add_item(item=x)
                    return view

                viewDisplay = {'overall': overallView, 'main': mainView, 'fieldmenu': fieldMenuView, 'field': fieldView, 'author': authorView, 'image': imageView, 'thumbnail': thumbnailView}
                
                embedMsg = await ctx.author.send(embed=discord.Embed(title="Processing..."))
                embedController = await ctx.author.send(embed=discord.Embed(title="Processing..."))
                view = createView(overallView)

                while True:
                    try:
                        await embedMsg.edit(embed=discord.Embed.from_dict(embed_dict))
                        await embedController.edit(embed=discord.Embed(title ='**🦎 | Server Lizard **:', description=controllerText), view=view)
                    except discord.HTTPException:
                        await embedMsg.edit(embed=discord.Embed.from_dict(oldEmbed))
                        embed_dict = deepcopy(oldEmbed)
                        index = controllerText.index('\n\n') + 2
                        await embedController.edit(embed=discord.Embed(title ='**🦎 | Server Lizard **:', description=controllerText[:index] + "Total number of characters exceeded 6000 characters. Please reduce the number of characters or fields."), view=view)                        

                    def checkButton(m):
                        return m.message == embedController and m.user == ctx.author

                    try:
                        interacted = await client.wait_for('interaction', timeout=3600, check=checkButton)
                    except asyncio.TimeoutError:
                        view.clear_items()
                        await embedController.edit(embed=discord.Embed(title="TIMED OUT"), view=view)
                    else:
                        await interacted.response.defer()
                        view.clear_items()
                        getButtonData = interacted.data['custom_id'].split(" ")
                        match getButtonData[0]:
                            case "section":
                                if getButtonData[1] == "field":
                                    sectionValue = None
                                    currentField = int(getButtonData[2])
                                    controllerText = f'Navigating [{section}] -> [field {currentField + 1}]'
                                    view = createView(fieldView)

                                elif getButtonData[1] == "fieldmenu" and currentField is not None and sectionValue is not None:
                                    sectionValue = None
                                    controllerText = f'Navigating [{section}] -> [field {currentField + 1}]'
                                    view = createView(fieldView)

                                else:
                                    section = getButtonData[1]
                                    sectionValue = None
                                    currentField = None
                                    controllerText = f'Navigating [{section}]'
                                    view = createView(viewDisplay[section])

                            case "value":
                                if currentField is None:
                                    sectionValue = getButtonData[1]
                                    controllerText = f'Navigating [{section}] -> [{sectionValue}]'
                                    if getButtonData[2] == "regular":
                                        valueType = 'regular'
                                        view = createView(valueView)
                                    else:
                                        valueType = 'perm'
                                        view = createView(valuePermView)
                                else:
                                    sectionValue = getButtonData[1]
                                    controllerText = f'Navigating [{section}] -> [field {currentField + 1}] -> [{sectionValue}]'

                                    if sectionValue == "inline":
                                        view = createView(inlineView)
                                    else:
                                        valueType = 'perm'
                                        view = createView(valuePermView)
                                
                            case "field":
                                if getButtonData[1] == "add":
                                    if addField() == False:
                                        controllerText = f'Navigating [{section}]\n\nYou cannot add any more fields.'
                                    else:
                                        controllerText = f'Navigating [{section}]\n\nField added.'
                                    view = createView(viewDisplay[section])

                                elif getButtonData[1] == "remove":
                                    embed_dict["fields"].pop(currentField)
                                    controllerText = f'Navigating [{section}]\n\nField {currentField + 1} removed.'
                                    view = createView(viewDisplay[section])

                            case "inline":
                                if getButtonData[1] == "true":
                                    embed_dict["fields"][currentField]["inline"] = True
                                    controllerText = f'Navigating [{section}] -> [field {currentField + 1}] -> [inline]\n\nInline set to True.'
                                    view = createView(inlineView)

                                elif getButtonData[1] == "false":
                                    embed_dict["fields"][currentField]["inline"] = False
                                    controllerText = f'Navigating [{section}] -> [field {currentField + 1}] -> [inline]\n\nInline set to False.'
                                    view = createView(inlineView)


                            case "execute":
                                if getButtonData[1] == "add":
                                    if sectionValue == "color":
                                        controllerText = f'Navigating [{section}] -> [{sectionValue}]\n\nAdding/Editing [{sectionValue}]. Please enter a 6 character color hex code (e.g. `F18FG3`).'
                                    else:
                                        controllerText = f'Navigating [{section}] -> [{sectionValue}]\n\nAdding/Editing [{sectionValue}]. Please type out the value you wish to input.'
                                    await embedController.edit(embed=discord.Embed(title ='**🦎 | Server Lizard **:', description=controllerText), view=view)

                                    def check(m):
                                        return m.channel.type is discord.ChannelType.private and m.author == ctx.author
                                    try:
                                        interacted = await client.wait_for('message', timeout=3600, check=check)
                                    except asyncio.TimeoutError:
                                        await embedController.edit(embed=discord.Embed(title="TIMED OUT"), view=view)
                                    else:
                                        oldEmbed = deepcopy(embed_dict)
                                        if sectionValue == "color":
                                            try:
                                                if interacted.content.isalnum() and len(interacted.content) == 6:
                                                    controllerText = editValue(int(interacted.content, base=16))
                                                else:
                                                    controllerText = f'Navigating [{section}] -> [{sectionValue}]\n\nInvalid input entered.'
                                            except:
                                                controllerText = f'Navigating [{section}] -> [{sectionValue}]\n\nInvalid input entered.'
                                        else:
                                            if sectionValue == "title" or sectionValue == "name":
                                                controllerText = editValue(interacted.content,256)
                                            elif sectionValue == "value":
                                                controllerText = editValue(interacted.content,1024)
                                            elif sectionValue == "description":
                                                controllerText = editValue(interacted.content,4096)
                                            else:
                                                controllerText = editValue(interacted.content,1000)

                                        if valueType == 'regular':
                                            view = createView(valueView)
                                        else:
                                            view = createView(valuePermView)
                    
                                elif getButtonData[1] == "remove":
                                    controllerText = f'Navigating [{section}] -> [{sectionValue}]\n\nRemoved [{sectionValue}].'
                                    deleteValue()
                                    if valueType == 'regular':
                                        view = createView(valueView)
                                    else:
                                        view = createView(valuePermView)

                                elif getButtonData[1] == "section":
                                    if getButtonData[2] == "add":
                                        addSection()
                                        controllerText = f'Navigating [{section}]\n\n[{section}] section added.'
                                        view = createView(viewDisplay[section])

                                    elif getButtonData[2] == "remove":
                                        deleteSection()
                                        controllerText = f'Navigating [{section}]\n\n[{section}] section removed.'
                                        view = createView(viewDisplay[section])

                                elif getButtonData[1] == "create":
                                    if arg.lower() == "create":
                                        controllerText = f'Creating embedded message in `#{ctx.channel.name}` on {ctx.guild.name}... hang on!'
                                        createdEmbed = await ctx.channel.send(embed=discord.Embed(title="Processing..."))
                                        embed_dict["footer"]["text"] = f'created by {ctx.author.display_name} | Message ID: {createdEmbed.id}'
                                        await createdEmbed.edit(embed=discord.Embed.from_dict(embed_dict))
                                        controllerText = f'Message created! [Link to message]({createdEmbed.jump_url})'
                                        await embedController.edit(embed=discord.Embed(title ='**🦎 | Server Lizard **:', description=controllerText), view=view)
                                        break

                                    elif arg.lower() == "edit":
                                        await fetchedMessage.edit(embed=discord.Embed.from_dict(embed_dict))
                                        controllerText = f'Message edited! [Link to message]({fetchedMessage.jump_url})'
                                        await embedController.edit(embed=discord.Embed(title ='**🦎 | Server Lizard **:', description=controllerText), view=view)
                                        break

                                elif getButtonData[1] == "cancel":
                                    controllerText = f'Embed creation cancelled'
                                    await embedController.edit(embed=discord.Embed(title ='**🦎 | Server Lizard **:', description=controllerText), view=view)
                                    break
                                else:
                                    print("Something wrong happened")
                            case _:
                                print("Something wrong happened")

            elif arg.lower() == "delete":
                try:
                    fetchedMessage = await ctx.channel.fetch_message(arg2)
                except:
                    await ctx.reply("Message not found. Please ensure that you're entering this command in the channel that the message is in, and use the following format: !embed edit [msg id]. The message ID can be found in the embed's footer")
                    return
                else:
                    embed_dict = fetchedMessage.embeds[0].to_dict()

                    if f'Message ID: {fetchedMessage.id}' in embed_dict["footer"]["text"] and fetchedMessage.author.id == 1032276665092538489:
                        pass
                    else:
                        await ctx.reply("That message is not a custom embedded message created by Server Lizard.")
                        return
                
                view = discord.ui.View()
                button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                view.add_item(item=button1)
                view.add_item(item=button2)
                msg1 = await ctx.reply(embed=discord.Embed(title=f'Delete Embedded Message (id: {fetchedMessage.id})?', description=f'[Link to message]({fetchedMessage.jump_url})'), view=view)
                def checkButton(m):
                    return m.message == msg1 and m.user == ctx.author

                try:
                    interacted = await client.wait_for('interaction', timeout=3600, check=checkButton)
                except asyncio.TimeoutError:
                    view.clear_items()
                    await msg1.edit(embed=discord.Embed(title="TIMED OUT"), view=view)
                else:
                    await interacted.response.defer()
                    view.clear_items()

                    if interacted.data['custom_id'] == "confirm":
                        await fetchedMessage.delete()
                        await msg1.edit(embed=discord.Embed(title="Embedded Message deleted"), view=view)
                    elif interacted.data['custom_id'] == "cancel":
                        await msg1.edit(embed=discord.Embed(title="Embed Deletion cancelled"), view=view)
            else:
                await ctx.reply("Please use the following format: `!embed create` / `!embed edit [msg id]` / `!embed delete [msg id]`", delete_after=20)