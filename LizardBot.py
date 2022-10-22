# bot.py
import os
import discord
from discord.ext import commands
from discord import Button, ButtonStyle
from dotenv import load_dotenv
import random
import asyncio
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta
import traceback

# Bot Settings
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

'''
# [BlahajCheck] Web Scraper Settings
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options, executable_path=r'/geckodriver') #comment out to disable webdriver loading
blahajURL = "https://www.ikea.com/sg/en/p/blahaj-soft-toy-shark-10373589/"
minihajURL = "https://www.ikea.com/sg/en/p/blahaj-soft-toy-shark-10373589/"
blahajFlat = ["https://i.redd.it/vg3vjkroytq71.jpg",
              "https://i.redd.it/2f72lz7qufm81.jpg",
              "https://i.redd.it/fxckzsfrivq71.png",
              "https://static.mothership.sg/1/2022/01/272744499_10165925896085402_5819381897009474509_n.jpeg"]
'''


# Universal Functions
def timeConvert(originalTime): #converts UTC to GMT+8
    newTime = originalTime + timedelta(hours=8)
    return newTime

# Bot Coding
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    #members = '\n - '.join([member.name for member in guild.members])
    #print(f'Guild Members:\n - {members}')


@client.command() #!admin
async def admin(ctx):
    for r in ctx.author.roles:
        if r.id == 423458739656458243 or r.id == 407557898638589974: #change according to mod role id
            await ctx.message.delete()
            embed=discord.Embed(title=f'Admin commands for Server Lizard', description='To use a command, enter: `!{command}`',color=0x14AB49)
            embed.add_field(name='📰 **Message Management**', value='`bulkdelete`', inline=False)
            await ctx.author.send(embed=embed)
            
client.remove_command('help')
@client.command(aliases=['command','help']) #!commands            
async def commands(ctx):
    embed=discord.Embed(title=f'Lizard Commands!', description='Use !help or !commands to show this list.\nTo use a command, enter: `!{command}`',color=0x14AB49)
    embed.add_field(name='🎲 **Games**', value='`roll` `game` `battle`', inline=False)
    embed.add_field(name='📰 **Message Management**', value='`timed` `selfdelete`', inline=False)
    embed.add_field(name='🙃 **Fluff**', value='`test` `greet` `change` ~~`blahaj`~~', inline=False)
    embed.add_field(name='👓 **Mod/Admin Use**', value='`admin`', inline=False)
    embed.add_field(name='**Additional Features**', value='Starboard', inline=False)
    await ctx.reply(embed=embed)

@client.command() #!test
async def test(ctx):
    await ctx.send("owo")

@client.command() #!history
async def history(ctx):
    messages = [str(x.author) + ": " + str(x.content) async for x in ctx.history(limit=123)]
    print(messages)

@client.command() #!change
async def change(ctx):
    roll = random.randint(1, 20)
    if roll > 4:
        myname = "Server Li" + ("z" * random.randint(0,13)) + "ard"
        await ctx.send(f"Changed name to {myname}!")
    elif roll == 4:
        myname = "L̶̨͐͋i̵̙̳̹̾͒͝z̷͓̰̗̃̇a̸͕̒ŕ̸͍̙̣͘d̤̙͖"
        await ctx.send(f"₵Ⱨ₳₦₲ɆĐ ₦₳₥Ɇ ₮Ø ₴ɆⱤVɆⱤ {myname}")
    elif roll == 3:
        myname = "🤖🦎"
        await ctx.send(f"** **📝🔄➡🤖🦎")
    elif roll <= 2:
        myname = ""
        await ctx.send(f"Stop changing my name! 😠")
    await ctx.guild.me.edit(nick=myname)
    
@client.command() #!greet
async def greet(ctx):
    channel = ctx.channel
    mymsg = await ctx.reply('Say hello!')

    def check(m):
        return m.content == 'hello' and m.channel == channel

    try:
        msg = await client.wait_for('message', timeout=20, check=check)
    except asyncio.TimeoutError:
        await mymsg.edit(content='Timed out!')
    else:
        await msg.reply(f'Hello {msg.author.display_name}!')
            
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

@client.command() #!battle
async def battle(ctx):
    try:
        getOpponentId = ctx.message.content.replace('!battle <@','')
        getOpponentId = int(getOpponentId.replace('>',''))
        guild = await client.fetch_guild(ctx.guild.id)
        getUser = await guild.fetch_member(getOpponentId)
        if ctx.guild.get_member(getOpponentId) is not None:
            if getUser != ctx.author and getUser.id != 1032276665092538489:
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

            elif getUser.id == 1032276665092538489:
                await ctx.reply('Use !game to battle me!')
            else:
                await ctx.reply('You cannot battle yourself!')
        else:
            await ctx.reply('Invalid syntax! Please use `!battle {@user}`')
    except:
        await ctx.reply('Invalid syntax! Please use `!battle {@user}`')
        
'''                        
@client.command() #!blahaj
async def blahaj(ctx):

    def searchStore(storeNo):
        mySearch = driver.find_element(By.XPATH, storeNo)
        myResult = mySearch.find_element(By.CLASS_NAME, 'pip-stockcheck__store-text')
        return myResult

    def cleanUpText(mytext):
        if (mytext == "Store - Out of stock."):
            return("Out of Stock")
        else:
            return(mytext)

    def cleanUpTextOnline(mytext):
        if (mytext == "Currently unavailable"):
            return("Unavailable")
        else:
            return(mytext)

    def findShark(myURL):
        driver.get(myURL)
        driver.execute_script("document.querySelector('.hnf-banner__container').style.display = 'none';") #hide cookies banner


        p_element = driver.find_element(By.CLASS_NAME, 'pip-delivery__text')
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(lambda d: 'pip-delivery__text--grey' not in p_element.get_attribute('class'))
        except:
            print("Derped")
            pass

        p_element = driver.find_element(By.CLASS_NAME, 'pip-delivery__text')
        p_element = cleanUpTextOnline(p_element.text)
        driver.find_element(By.CLASS_NAME, 'pip-stockcheck__text').click()

        alexandra = cleanUpText(searchStore('//label[@for="store_045"]').text)
        jurong = cleanUpText(searchStore('//label[@for="store_650"]').text)
        tampines = cleanUpText(searchStore('//label[@for="store_022"]').text)
        return(p_element, alexandra, jurong, tampines)

    blahajAvail = {}
    minihajAvail = {}
    blahajAvail["online"], blahajAvail["alexandra"], blahajAvail["jurong"], blahajAvail["tampines"] = findShark(blahajURL)
    minihajAvail["online"], minihajAvail["alexandra"], minihajAvail["jurong"], minihajAvail["tampines"] = findShark(minihajURL)
    if (blahajAvail["alexandra"] == blahajAvail["jurong"] == blahajAvail["tampines"] == minihajAvail["alexandra"] == minihajAvail["jurong"] == minihajAvail["tampines"] == "Out of Stock" and blahajAvail["online"] == minihajAvail["online"] == "Unavailable"):
        embedColour = 0xFF5733
        embedImage = blahajFlat[random.randint(0,3)]
    else:
        embedColour = 0x00FF00
        embedImage = "https://www.ikea.com/sg/en/images/products/blahaj-soft-toy-shark__0710175_pe727378_s5.jpg"
        
    embed=discord.Embed(title="BLÅHAJ Availability", description="Get your BLÅHAJ before they're gone!\n[BLÅHAJ (100cm)](https://www.ikea.com/sg/en/p/blahaj-soft-toy-shark-10373589/)\n[MINIHAJ (55cm)](https://www.ikea.com/sg/en/p/blahaj-soft-toy-shark-10373589/)", color=embedColour)
    embed.set_image(url=embedImage)
    embed.add_field(name="BLÅHAJ", value="> Online: " + blahajAvail["online"] + "\n> Alexandra: " + blahajAvail["alexandra"] + "\n> Jurong: " + blahajAvail["jurong"] + "\n> Tampines: " + blahajAvail["tampines"], inline=True)
    embed.add_field(name="MINIHAJ", value="> Online: " + minihajAvail["online"] + "\n> Alexandra: " + minihajAvail["alexandra"] + "\n> Jurong: " + minihajAvail["jurong"] + "\n> Tampines: " + minihajAvail["tampines"], inline=True)
    await ctx.send(embed=embed)
'''
@client.command() #!bulkdelete        
async def bulkdelete(ctx):
    for r in ctx.author.roles:
        if r.id == 423458739656458243  or r.id == 407557898638589974: #change according to mod role id
            await ctx.message.delete()
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
                interacted = await client.wait_for('interaction', timeout=60, check=checkButton)
            except asyncio.TimeoutError:
                view.clear_items()
                await mymsg.edit(content='Timed out!', view=view)
            else:
                await interacted.response.defer()
                view.clear_items()
                await mymsg.edit(view=view)

                if interacted.data['custom_id'] == 'confirm':
                    embed = discord.Embed(title=f'Please enter the URL link to the first message to start from', description=f'example: <https://discord.com/channels/123456789012345678/1234567890123456789/1234567890123456789>', color=0xFF5733)
                    msg2 = await ctx.author.send(embed=embed)

                    def check(m):
                        return "http" in m.content and m.channel.type is discord.ChannelType.private and m.author == ctx.author
                    try:
                        msg3 = await client.wait_for('message', timeout=300, check=check)
                    except asyncio.TimeoutError:
                        await msg2.edit(content='Timed out!')
                    else:
                        try:
                            getLink = msg3.content.replace("https://discord.com/channels/","")
                            idList = getLink.split("/")
                            guildId = int(idList[0])
                            channelId = int(idList[1])
                            messageId = int(idList[2])

                            myGuild = client.get_guild(guildId)
                            myChannel = client.get_channel(channelId)
                            fetched = await myChannel.fetch_message(messageId)
                        except:
                            embed=discord.Embed(title=f'Error, could not retrieve message', description=f'Bulk delete cancelled', color=0xFF5733)
                            await ctx.author.send(embed=embed)
                        else:
                            embed=discord.Embed(title=f"Bulk Delete [Start]", description="**Server**: " + str(myGuild) + "\n**Channel**: #" + str(myChannel) + "\n**Author**: " + str(fetched.author) + "\n**Time**: " + timeConvert(fetched.created_at).strftime("%d %B %Y, %I:%M:%S%p"), color=0xFF5733)
                            embed.add_field(name="Message Link", value=f"> [\[Link\]]({fetched.jump_url})", inline=False)
                            embed.add_field(name="Message Content", value=f"> {fetched.content}", inline=False)
                            await ctx.author.send(embed=embed)
                            embed=discord.Embed(title=f'Please enter the URL link to the last message to end at', description=f'example: <https://discord.com/channels/123456789012345678/1234567890123456789/1234567890123456789>', color=0xFF5733)
                            msg4 = await ctx.author.send(embed=embed)

                            try:
                                msg5 = await client.wait_for('message', timeout=300, check=check)
                            except asyncio.TimeoutError:
                                await msg4.edit(content='Timed out!')
                            else:
                                try:
                                    getLink = msg5.content.replace("https://discord.com/channels/","")
                                    idList = getLink.split("/")
                                    guildId2 = int(idList[0])
                                    channelId2 = int(idList[1])
                                    messageId2 = int(idList[2])

                                    myChannel2 = client.get_channel(channelId2)
                                    fetched2 = await myChannel2.fetch_message(messageId2)
                                except:
                                    embed=discord.Embed(title=f'Error, could not retrieve message', description=f'Bulk delete cancelled', color=0xFF5733)
                                    await ctx.author.send(embed=embed)
                                else:
                                    if channelId2 != channelId:
                                        embed=discord.Embed(title=f'Error, this message belongs to a different channel', description=f'Bulk delete cancelled', color=0xFF5733)
                                        await ctx.author.send(embed=embed)
                                    else:
                                        embed=discord.Embed(title=f"Bulk Delete [End]", description="**Server**: " + str(myGuild) + "\n**Channel**: #" + str(myChannel) + "\n**Author**: " + str(fetched2.author) + "\n**Time**: " + timeConvert(fetched2.created_at).strftime("%d %B %Y, %I:%M:%S%p"), color=0xFF5733)
                                        embed.add_field(name="Message Link", value=f"> [\[Link\]]({fetched2.jump_url})", inline=False)
                                        embed.add_field(name="Message Content", value=f"> {fetched2.content}", inline=False)
                                        await ctx.author.send(embed=embed)

                                        if fetched.created_at < fetched2.created_at:
                                            dateStart = fetched.created_at - timedelta(seconds=0.1)
                                            dateEnd = fetched2.created_at + timedelta(seconds=0.1)
                                        else:
                                            dateStart = fetched2.created_at - timedelta(seconds=0.1)
                                            dateEnd = fetched.created_at + timedelta(seconds=0.1)

                                        messages = [message async for message in myChannel.history(limit=3000, before=dateEnd, after=dateStart)]

                                        view.add_item(item=button1)
                                        view.add_item(item=button2)
                                        embed=discord.Embed(title=f"Delete {len(messages)} messages?", description="(Search Limit: 3000 messages from start date)\n\n**Server**: " + str(myGuild) + "\n**Channel**: #" + str(myChannel), color=0xFF5733)
                                        embed.add_field(name="Date", value=f"> **Start**: " + timeConvert(dateStart).strftime("%d %B %Y, %I:%M:%S%p") + "\n> **End**: " + timeConvert(dateEnd).strftime("%d %B %Y, %I:%M:%S%p"), inline=False)
                                        msg6 = await ctx.author.send(embed=embed, view=view)

                                        def checkButton2(m):
                                            return m.message == msg6 and m.user == ctx.author

                                        try:
                                            interacted = await client.wait_for('interaction', timeout=60, check=checkButton2)
                                        except asyncio.TimeoutError:
                                            view.clear_items()
                                            await msg6.edit(content='Timed out!', view=view)
                                        else:
                                            await interacted.response.defer()
                                            view.clear_items()
                                            await msg6.edit(view=view)

                                            if interacted.data['custom_id'] == 'confirm':
                                                embed=discord.Embed(title=f'Processing...', color=0xFF5733)
                                                progress = await ctx.author.send(embed=embed)
                                                deleted = await myChannel.purge(limit=3000, before=dateEnd, after=dateStart)
                                                await myChannel.send(f'Deleted {len(deleted)} message(s).')
                                                embed=discord.Embed(title=f'{len(deleted)} messages deleted from #{myChannel} in {myGuild}', color=0x00FF00)
                                                await progress.edit(embed=embed)
                                            elif interacted.data['custom_id'] == 'cancel':
                                                embed=discord.Embed(title=f'Bulk delete cancelled', color=0xFF5733)
                                                await ctx.author.send(embed=embed)                                                

                elif interacted.data['custom_id'] == 'cancel':
                    embed=discord.Embed(title=f'Bulk delete cancelled', color=0xFF5733)
                    await ctx.author.send(embed=embed)

@client.command() #!selfdelete        
async def selfdelete(ctx):
    await ctx.message.delete()
    view = discord.ui.View()
    button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
    button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
    view.add_item(item=button1)
    view.add_item(item=button2)
    embed = discord.Embed(title=f'__**You are attempting to bulk delete your messages from a channel**__', description=f'Do you wish to proceed?', color=0xFF5733)
    mymsg = await ctx.author.send(embed=embed, view=view)

    def checkButton(m):
        return m.message == mymsg and m.user == ctx.author

    try:
        interacted = await client.wait_for('interaction', timeout=60, check=checkButton)
    except asyncio.TimeoutError:
        view.clear_items()
        await mymsg.edit(content='Timed out!', view=view)
    else:
        await interacted.response.defer()
        view.clear_items()
        await mymsg.edit(view=view)

        if interacted.data['custom_id'] == 'confirm':
            embed = discord.Embed(title=f'Please enter the URL link to the first message to start from', description=f'example: <https://discord.com/channels/123456789012345678/1234567890123456789/1234567890123456789>', color=0xFF5733)
            msg2 = await ctx.author.send(embed=embed)

            def check(m):
                return "http" in m.content and m.channel.type is discord.ChannelType.private and m.author == ctx.author
            try:
                msg3 = await client.wait_for('message', timeout=300, check=check)
            except asyncio.TimeoutError:
                await msg2.edit(content='Timed out!')
            else:
                try:
                    getLink = msg3.content.replace("https://discord.com/channels/","")
                    idList = getLink.split("/")
                    guildId = int(idList[0])
                    channelId = int(idList[1])
                    messageId = int(idList[2])

                    myGuild = client.get_guild(guildId)
                    myChannel = client.get_channel(channelId)
                    fetched = await myChannel.fetch_message(messageId)
                    # Author: str(fetched.author)
                    # Message: fetched.content
                    # Channel: str(fetched.channel)
                except:
                    await ctx.author.send("Error, could not retrieve message.")
                else:
                    if fetched.author != ctx.author:
                        await ctx.author.send("Error, this message does not belong to you.")
                    else:
                        embed=discord.Embed(title=f"Bulk Delete (own messages) [Start]", description="**Server**: " + str(myGuild) + "\n**Channel**: #" + str(myChannel) + "\n**Time**: " + timeConvert(fetched.created_at).strftime("%d %B %Y, %I:%M:%S%p"), color=0xFF5733)
                        embed.add_field(name="Message Link", value=f"> [\[Link\]]({fetched.jump_url})", inline=False)
                        embed.add_field(name="Message Content", value=f"> {fetched.content}", inline=False)
                        await ctx.author.send(embed=embed)
                        embed=discord.Embed(title=f'Please enter the URL link to the last message to end at', description=f'example: <https://discord.com/channels/123456789012345678/1234567890123456789/1234567890123456789>', color=0xFF5733)
                        msg4 = await ctx.author.send(embed=embed)

                        try:
                            msg5 = await client.wait_for('message', timeout=300, check=check)
                        except asyncio.TimeoutError:
                            await msg4.edit(content='Timed out!')
                        else:
                            try:
                                getLink = msg5.content.replace("https://discord.com/channels/","")
                                idList = getLink.split("/")
                                guildId2 = int(idList[0])
                                channelId2 = int(idList[1])
                                messageId2 = int(idList[2])

                                myChannel2 = client.get_channel(channelId2)
                                fetched2 = await myChannel2.fetch_message(messageId2)
                            except:
                                embed=discord.Embed(title=f'Error, could not retrieve message', description=f'Bulk delete cancelled', color=0xFF5733)
                                await ctx.author.send(embed=embed)
                            else:
                                if channelId2 != channelId:
                                    embed=discord.Embed(title=f'Error, this message belongs to a different channel', description=f'Bulk delete cancelled', color=0xFF5733)
                                    await ctx.author.send(embed=embed)
                                else:
                                    if fetched2.author != ctx.author:
                                        embed=discord.Embed(title=f'Error, this message does not belong to you', description=f'Bulk delete cancelled', color=0xFF5733)
                                        await ctx.author.send(embed=embed)
                                    else:
                                        embed=discord.Embed(title=f"Bulk Delete (own messages) [End]", description="**Server**: " + str(myGuild) + "\n**Channel**: #" + str(myChannel2) + "\n**Time**: " + timeConvert(fetched2.created_at).strftime("%d %B %Y, %I:%M:%S%p"), color=0xFF5733)
                                        embed.add_field(name="Message Link", value=f"> [\[Link\]]({fetched2.jump_url})", inline=False)
                                        embed.add_field(name="Message Content", value=f"> {fetched2.content}", inline=False)
                                        await ctx.author.send(embed=embed)

                                        embed=discord.Embed(title=f"Calculating...", color=0xFF5733)
                                        msg6 = await ctx.author.send(embed=embed)

                                        if fetched.created_at < fetched2.created_at:
                                            dateStart = fetched.created_at - timedelta(seconds=0.1)
                                            dateEnd = fetched2.created_at + timedelta(seconds=0.1)
                                        else:
                                            dateStart = fetched2.created_at - timedelta(seconds=0.1)
                                            dateEnd = fetched.created_at + timedelta(seconds=0.1)
                                        def checkUser(m):
                                                    return m.author == ctx.author

                                        counter = 0
                                        async for x in myChannel.history(limit=3000, before=dateEnd, after=dateStart):
                                            if x.author == ctx.author:
                                                counter += 1

                                        view.add_item(item=button1)
                                        view.add_item(item=button2)
                                        embed=discord.Embed(title=f"Delete {counter} messages?", description="(Search Limit: 3000 messages from start date)\n\n**Server**: " + str(myGuild) + "\n**Channel**: #" + str(myChannel), color=0xFF5733)
                                        embed.add_field(name="Date", value=f"> **Start**: " + timeConvert(dateStart).strftime("%d %B %Y, %I:%M:%S%p") + "\n> **End**: " + timeConvert(dateEnd).strftime("%d %B %Y, %I:%M:%S%p"), inline=False)
                                        await msg6.edit(embed=embed, view=view)

                                        def checkButton2(m):
                                            return m.message == msg6 and m.user == ctx.author

                                        try:
                                            interacted = await client.wait_for('interaction', timeout=60, check=checkButton2)
                                        except asyncio.TimeoutError:
                                            view.clear_items()
                                            await msg6.edit(content='Timed out!', view=view)
                                        else:
                                            await interacted.response.defer()
                                            view.clear_items()
                                            await msg6.edit(view=view)

                                            if interacted.data['custom_id'] == 'confirm':
                                                embed=discord.Embed(title=f'Processing...', color=0xFF5733)
                                                progress = await ctx.author.send(embed=embed)
                                                deleted = await myChannel.purge(limit=3000, before=dateEnd, after=dateStart, check=checkUser)
                                                embed=discord.Embed(title=f'{len(deleted)} messages deleted from #{myChannel} in {myGuild}', color=0x00FF00)
                                                await progress.edit(embed=embed)
                                            elif interacted.data['custom_id'] == 'cancel':
                                                embed=discord.Embed(title=f'Bulk delete cancelled', color=0xFF5733)
                                                await ctx.author.send(embed=embed)
                        
        elif interacted.data['custom_id'] == 'cancel':
            embed=discord.Embed(title=f'Bulk delete cancelled', color=0xFF5733)
            await ctx.author.send(embed=embed)

@client.command() #!timed        
async def timed(ctx):
    try:
        countdown = ctx.message.content.replace('!timed ', '')
        myList = countdown.split(' ')
        countdown = float(myList[0])
        msg = await ctx.reply(f'Message set to auto-delete in {countdown} minutes')
    except:
        countdown = 5
        msg = await ctx.reply(f'Syntax error! Defaulting to auto-deletion in 5 minutes. Please use !timed # (# = minutes)')
    await asyncio.sleep(countdown * 60)
    await msg.delete()
    await ctx.message.delete()

@client.command()
async def roll(ctx):
    try:
        number = int(ctx.message.content.replace('!roll ',''))
        if number > 0:
            result = random.randint(1,number)
            await ctx.reply(f'🎲 Rolled {result}! 🎲')
        else:
            await ctx.reply(f'Please enter a valid number!')
    except:
        await ctx.reply('Please enter a positive number after !roll.')
        
@client.event
async def on_message(message):
    if message.channel.type is discord.ChannelType.private:
        prefix = 'DM'
    else:
        prefix = str(message.guild) + " #" + str(message.channel)
    print(f"[{prefix}] " + str(message.author) + ": " + str(message.content))

    if '<@1032276665092538489>' in message.content and '!battle' not in message.content:
        roll = random.randint(1, 10)
        if roll > 4:
            await message.channel.send('*slithers by*')
        elif roll == 3:
            await message.channel.send('*blends into the surroundings*')
        elif roll == 2:
            await message.channel.send('*munches on some bread*')
        elif roll == 1:
            await message.reply('*bonks you* <:bonk:687841666182414413>')
 
#@mod
    if ('<@&423458739656458243>' in message.content or '<@&1030144135560167464>' in message.content) and message.author.id != 1032276665092538489:
        reportChannel = discord.utils.get(message.guild.channels, name='infractions')
        embed=discord.Embed(title=f"@mod pinged by {message.author.display_name}", description=f"[\[Link\]]({message.jump_url})", color=0x00FF00)
        embed.set_footer(text=timeConvert(datetime.utcnow()).strftime("%d %B %Y, %I:%M:%S%p"))
        await reportChannel.send(embed=embed)
        await message.reply('Mods pinged!')

    await client.process_commands(message)

class ReportModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Details on why this post was reported", style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Additional supporting links/messages", style=discord.InputTextStyle.long, required=False))

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message('Report received.', ephemeral=True, delete_after=30)

@client.message_command(name="Report Message")
async def report(ctx: discord.ApplicationContext, message: discord.Message):
    report = ReportModal(title="Report Form")
    await ctx.send_modal(report)
    await report.wait()
    embed = discord.Embed(title=f'__**Post report by {ctx.user.display_name} ({ctx.user})**__', description=f'**Reported User**: {str(message.author.display_name)} ({message.author})\n**Channel**: #{str(message.channel)}\n**Time**: ' + timeConvert(message.created_at).strftime("%d %B %Y, %I:%M:%S%p") + f'\n**Message Link**: [\[Link\]]({message.jump_url})', color=0xFF5733)
    embed.add_field(name="Message Content", value=f"> `{message.content}`", inline=False)
    embed.add_field(name="Reporting Details", value=report.children[0].value, inline=False)
    if report.children[1].value != "":
        additionalInfo = report.children[1].value
    else:
        additionalInfo = 'N/A'
    embed.add_field(name="Additional Info", value=additionalInfo, inline=False)
    reportChannel = discord.utils.get(ctx.guild.channels, name='infractions')
    await reportChannel.send(embed=embed)
  
@client.event
async def on_reaction_add(reaction,user):
    if reaction.emoji == '⭐': #nsfw-starboard
        reaction = discord.utils.get(reaction.message.reactions, emoji='⭐')
        if (reaction.message.channel.id == 407561378564407297 or reaction.message.channel.id == 407561306162331674) and reaction.count >= 5:
            doNotAdd = 0
            async for user in reaction.users():
                if user.id == 1032276665092538489:
                    doNotAdd = 1
                    break
            if doNotAdd == 0:
                await reaction.message.add_reaction('⭐')
                starChannel = discord.utils.get(reaction.message.guild.channels, name='nsfw-starboard')
                embed=discord.Embed(description=f'{reaction.message.content}\n\n> [\[Link\]]({reaction.message.jump_url})', color=0x14AB49)
                embed.set_footer(text=f'brought to you by degens at #{reaction.message.channel}')
                embed.set_author(name=f'⭐⭐{reaction.message.author.display_name}⭐⭐', icon_url=reaction.message.author.display_avatar)
                if reaction.message.attachments:
                    embed.set_image(url=reaction.message.attachments[0].url)
                await starChannel.send(embed=embed)

client.run(TOKEN)
