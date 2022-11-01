# bot.py
import os
import discord
from discord.ext import commands
from discord import Button, ButtonStyle
from dotenv import load_dotenv
import random
import asyncio
import requests
import json
from datetime import datetime, timedelta
import time
import math
#import mysql.connector

#### Bot Settings
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

#### Global Functions
def timeConvert(originalTime): #converts UTC to GMT+8
    newTime = originalTime + timedelta(hours=8)
    return newTime

#usage example: checkRoles(ctx.author, [1030144135560167464, 1035245311553196112])
#returns True if any of the roles in the array matches, else return False
def checkRoles(member, arr):
    for x in member.roles:
        for y in arr:
            if x.id == y:
                return True
    return False

#### Bot Coding
@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )

'''
mydb = mysql.connector.connect(
  host=os.getenv('SQL_HOST'),
  user=os.getenv('SQL_USER'),
  password=os.getenv('SQL_PASSWORD'),
  database=os.getenv('SQL_DATABASE'),
  port=os.getenv('SQL_PORT')
)

mycursor = mydb.cursor()

@client.command() #!sql tables
async def makeTable(ctx):
    mycursor.execute("CREATE TABLE testingtable (memberId BIGINT, \
lastActivity INT(255), \
verified INT(1), \
expired INT(1), \
")

@client.command()
async def populateTable(ctx):
    sql = "INSERT INTO testingtable (memberId, lastActivity, verified, expired) VALUES (%s, %s, %s, %s)"
    
    for x in ctx.guild.members:
        memberName = x.name + '#' + x.discriminator
        memberId = x.id
        lastActivity = time.time()
        verified = 0
        for r in x.roles:
            if r.id == 1030144135560167464:
                verified = 1
        expired = 0
        print(f'Name: {x.name}#{x.discriminator}, ID: {x.id}, Verified: {verified}, Expired: {expired}')
        
        val = (memberId, lastActivity, verified, expired)
        mycursor.execute(sql, val)
        mydb.commit()
'''

@client.command()
async def populate(ctx): #populate the user profile channel
    if ctx.author.id == 262909760255426570:
        msg1 = await ctx.reply("Populating user profiles... sit tight!")
        channel = client.get_channel(1035131570257932318)
        for member in channel.guild.members:
            userName = member.name + "#" + member.discriminator
            roleList = []
            for x in member.roles:
                roleList.append(x.name)

            embed = discord.Embed(title=f'{member.display_name} ({userName})', description=f'**User ID**: {member.id}\n**User Roles**: {roleList}\n**Infractions**:')
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)
            await asyncio.sleep(2)
        await msg1.reply("All done!")
            

@client.event #update user profiles to a channel whenever there's a change
async def on_member_update(before, after):
    '''
    > activates upon member
        - leaving the server
        - changing nickname
        - changing roles
        - changing pfp
    
    > does not activate when member joins server
    '''
    channel = client.get_channel(1035131570257932318) #user profiles channel
    
    await asyncio.sleep(5)

    if after.guild.get_member(after.id) is not None and checkRoles(after, [454948280825282560]) == False: #update if member still in server, and does not have the new member role
        found = 0
        async for message in channel.history(limit=None): # If member profile is found, update it 
            if message.embeds and message.embeds[0].description and f'**User ID**: {after.id}' in message.embeds[0].description:
                found = 1
                mystr = message.embeds[0].description.split('**Infractions**:')
                if len(mystr) > 1:
                    infractions = mystr[1]
                else:
                    infractions = "" # no infractions

                userName = after.name + "#" + after.discriminator
                roleList = []
                for x in after.roles:
                    roleList.append(x.name)

                embed = discord.Embed(title=f'{after.display_name} ({userName})', description=f'**User ID**: {after.id}\n**User Roles**: {roleList}\n**Infractions**:{infractions}')
                embed.set_thumbnail(url=after.display_avatar.url)
                await message.edit(embed=embed)
                break

        if found == 0: #Profile not found, creating new profile
            userName = after.name + "#" + after.discriminator
            roleList = []
            for x in after.roles:
                roleList.append(x.name)

            embed = discord.Embed(title=f'{after.display_name} ({userName})', description=f'**User ID**: {after.id}\n**User Roles**: {roleList}\n**Infractions**:')
            embed.set_thumbnail(url=after.display_avatar.url)
            await channel.send(embed=embed)

            await asyncio.sleep(5)
            dupeCount = 0
            async for message in channel.history(limit=10): # Deletes duplicate profiles if found
                if message.embeds and message.embeds[0].description and f'**User ID**: {after.id}' in message.embeds[0].description:
                    dupeCount += 1
                    if dupeCount > 1:
                        await message.delete()

@client.event #if a user profile already exists, posts user's previous roles to the notice channel
async def on_member_join(member):
    profileChannel = client.get_channel(1035131570257932318)
    newcomerChannel = client.get_channel(535480699981922324)
    async for message in profileChannel.history(limit=None):
        if message.embeds:
            if message.embeds[0].description and f'**User ID**: {member.id}' in message.embeds[0].description:
                mystr = message.embeds[0].description.replace("\n**Infractions**:","")
                mystr = mystr.split("**User Roles**: ")
                embed = discord.Embed(title=f'{member.display_name} rejoined the server', description=f'Their roles were: {mystr[1]}')
                await newcomerChannel.send(embed=embed)
                break

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

@client.user_command(name="User Profile") #Looks up user's profile in the user profile channel
async def userProfile(ctx, user):
    if checkRoles(ctx.author, [423458739656458243, 407557898638589974]):
        channel = client.get_channel(1035124265411940392)
        found = 0
        
        async for message in channel.history(limit=None):
            if message.embeds and message.embeds[0].description and f'**User ID**: {user.id}' in message.embeds[0].description:
                await ctx.respond(f'User profile for {user.display_name} found at [\[link]]({message.jump_url})\nUser ID: {user.id}', ephemeral=True,delete_after=300)
                found = 1
                break
        if found == 0:
            await ctx.respond(f'Profile can\'t be found?! Contact your local lizard support', ephemeral=True,delete_after=30)
    else:
        await ctx.respond(f'You are not authorized to use this command', ephemeral=True,delete_after=30)
    
@client.command() #!admin
async def admin(ctx):
    if checkRoles(ctx.author, [423458739656458243, 407557898638589974]):
        await ctx.message.delete()
        embed=discord.Embed(title=f'Admin commands for Server Lizard', description='To use a command, enter: `!{command}`',color=0x14AB49)
        embed.add_field(name='📰 **Message Management**', value='`bulkdelete`', inline=False)
        embed.add_field(name='👓 **Administrative**', value='~~`roles`~~', inline=False)
        embed.add_field(name='❌ **Disciplinary**', value='`infraction add` `infraction remove`', inline=False)
        await ctx.author.send(embed=embed)
            
client.remove_command('help')
@client.command(aliases=['command','help']) #!commands            
async def commands(ctx):
    embed=discord.Embed(title=f'Lizard Commands!', description='Use !help or !commands to show this list.\nTo use a command, enter: `!{command}`',color=0x14AB49)
    embed.add_field(name='🎲 **Games**', value='`roll` `game` `battle`', inline=False)
    embed.add_field(name='📰 **Message Management**', value='`timed` `selfdelete`', inline=False)
    embed.add_field(name='🙃 **Fluff**', value='`test` `greet` `change` `blahaj`', inline=False)
    embed.add_field(name='👓 **Mod/Admin Use**', value='`admin`', inline=False)
    embed.add_field(name='**Additional Features**', value='Starboard / Post Reporting / Mod Pings', inline=False)
    await ctx.reply(embed=embed)

@client.command() #!test
async def test(ctx):
    await ctx.send("owo")

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
        if ctx.guild.get_member(getOpponentId) is None:
            await ctx.reply('Invalid syntax! Please use `!battle {@user}`')
        else:
            if getUser.id == 1032276665092538489:
                await ctx.reply('Use !game to battle me!')
            elif getUser != ctx.author:
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
        
@client.command() #!blahaj
async def blahaj(ctx):
    storeList = ['Tampines', 'Alexandra', 'Jurong', 'Online']

    url = 'https://api.ingka.ikea.com/cia/availabilities/ru/sg?itemNos=10373589&expand=StoresList,Restocks,SalesLocations'
    session = requests.Session()
    headers = {'authority': 'api.ingka.ikea.com',
    'method': 'GET',
    'path': '/cia/availabilities/ru/sg?itemNos=10373589&expand=StoresList,Restocks,SalesLocations',
    'scheme': 'https',
    'accept': 'application/json;version=2',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,ja;q=0.8',
    'dnt': '1',
    'origin': 'https://www.ikea.com',
    'referer': 'https://www.ikea.com/',
    'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52',
    'x-client-id': 'b6c117e5-ae61-4ef5-b4cc-e0b1e37f0631',
    }

    response = requests.get(url, headers=headers)
    mydict = json.loads(response.content.decode('utf-8'))

    blahajStock = {}
    for x in range(3):
        blahajStock[storeList[x]] = mydict['availabilities'][x]['buyingOption']['cashCarry']['availability']['probability']['thisDay']['messageType'].replace('_',' ')
    blahajStock[storeList[3]] = mydict['availabilities'][3]['buyingOption']['homeDelivery']['availability']['probability']['thisDay']['messageType'].replace('_',' ')

    url2 = 'https://api.ingka.ikea.com/cia/availabilities/ru/sg?itemNos=00540664&expand=StoresList,Restocks,SalesLocations'
    headers['path'] = '/cia/availabilities/ru/sg?itemNos=00540664&expand=StoresList,Restocks,SalesLocations'

    response = requests.get(url, headers=headers)
    mydict = json.loads(response.content.decode('utf-8'))


    minihajStock = {}
    for x in range(3):
        minihajStock[storeList[x]] = mydict['availabilities'][x]['buyingOption']['cashCarry']['availability']['probability']['thisDay']['messageType'].replace('_',' ')
    minihajStock[storeList[3]] = mydict['availabilities'][3]['buyingOption']['homeDelivery']['availability']['probability']['thisDay']['messageType'].replace('_',' ')
    
    blahajFlat = ["https://i.redd.it/vg3vjkroytq71.jpg",
              "https://i.redd.it/2f72lz7qufm81.jpg",
              "https://i.redd.it/fxckzsfrivq71.png",
              "https://static.mothership.sg/1/2022/01/272744499_10165925896085402_5819381897009474509_n.jpeg"]
    
    if (blahajStock['Tampines'] == blahajStock['Alexandra'] == blahajStock['Jurong'] == blahajStock['Online'] == minihajStock['Tampines'] == minihajStock['Alexandra'] == minihajStock['Jurong'] == minihajStock['Online'] == "OUT OF STOCK"):
        embedColour = 0xFF5733
        embedImage = blahajFlat[random.randint(0,3)]
    else:
        embedColour = 0x00FF00
        embedImage = "https://www.ikea.com/sg/en/images/products/blahaj-soft-toy-shark__0710175_pe727378_s5.jpg"
        
    embed=discord.Embed(title="BLÅHAJ Availability", description="Get your BLÅHAJ before they're gone!\n[BLÅHAJ (100cm)](https://www.ikea.com/sg/en/p/blahaj-soft-toy-shark-10373589/)\n[MINIHAJ (55cm)](https://www.ikea.com/sg/en/p/blahaj-soft-toy-shark-10373589/)", color=embedColour)
    embed.set_image(url=embedImage)
    embed.add_field(name="BLÅHAJ", value="> Online: " + blahajStock["Online"] + "\n> Alexandra: " + blahajStock["Alexandra"] + "\n> Jurong: " + blahajStock["Jurong"] + "\n> Tampines: " + blahajStock["Tampines"], inline=True)
    embed.add_field(name="MINIHAJ", value="> Online: " + minihajStock["Online"] + "\n> Alexandra: " + minihajStock["Alexandra"] + "\n> Jurong: " + minihajStock["Jurong"] + "\n> Tampines: " + minihajStock["Tampines"], inline=True)
    embed.set_footer(text=timeConvert(datetime.utcnow()).strftime("%d %B %Y, %I:%M:%S%p"))
    await ctx.send(embed=embed)

@client.command() #!bulkdelete   
async def bulkdelete(ctx):
    try:
        await ctx.message.delete()
    except:
        await ctx.author.send(f'Please use this command in a server channel.')
    else:
        if checkRoles(ctx.author, [423458739656458243, 407557898638589974]):
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
                        embed=discord.Embed(title=f"Bulk Delete [Start]", description="**Server**: " + str(fetched.guild) + "\n**Channel**: #" + str(fetched.channel) + "\n**Author**: " + str(fetched.author) + "\n**Time**: " + timeConvert(fetched.created_at).strftime("%d %B %Y, %I:%M:%S%p"), color=0xFF5733)
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
                        embed=discord.Embed(title=f"Bulk Delete [End]", description="**Server**: " + str(fetched2.guild) + "\n**Channel**: #" + str(fetched2.channel) + "\n**Author**: " + str(fetched2.author) + "\n**Time**: " + timeConvert(fetched2.created_at).strftime("%d %B %Y, %I:%M:%S%p"), color=0xFF5733)
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
                            messageArray.append({'message': shortMessage, 'time': timeConvert(x.created_at).strftime("%d/%m/%y %H:%M:%S")})

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
                        embedArray.add_field(name="Date", value=f"> **Start**: " + timeConvert(dateStart).strftime("%d %B %Y, %I:%M:%S%p") + "\n> **End**: " + timeConvert(dateEnd).strftime("%d %B %Y, %I:%M:%S%p"), inline=False)
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


@client.command() #!selfdelete        
async def selfdelete(ctx):
    try:
        await ctx.message.delete()
    except:
        await ctx.author.send("Please use this command in a server channel.")
    else:
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
                            if fetched.author != ctx.author:
                                await ctx.author.send(embed=discord.Embed(title="Error, this message does not belong to you. Please try again"))
                            else:
                                checkFirstMessage = 1

                if checkFirstMessage == 1:
                    embed=discord.Embed(title=f"Bulk Delete (own messages) [Start]", description="**Server**: " + str(fetched.guild) + "\n**Channel**: #" + str(fetched.channel) + "\n**Time**: " + timeConvert(fetched.created_at).strftime("%d %B %Y, %I:%M:%S%p"), color=0xFF5733)
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
                                elif fetched2.author != ctx.author:
                                    await ctx.author.send(embed=discord.Embed(title="Error, this message does not belong to you. Please try again"))
                                else:
                                    checkSecondMessage = 1

                if checkFirstMessage == 1 and checkSecondMessage == 1:
                    embed=discord.Embed(title=f"Bulk Delete (own messages) [End]", description="**Server**: " + str(fetched2.guild) + "\n**Channel**: #" + str(fetched2.channel) + "\n**Time**: " + timeConvert(fetched2.created_at).strftime("%d %B %Y, %I:%M:%S%p"), color=0xFF5733)
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
                    def checkUser(m):
                        return m.author.id == ctx.author.id

                    messageArray = []
                    messagePreview = ""
                    async for x in fetched.channel.history(limit=3000, before=dateEnd, after=dateStart):
                        if x.author.id == ctx.author.id:
                            if len(x.content) > 27:
                                shortMessage = x.content[:27] + ".."
                            else:
                                shortMessage = x.content
                            messageArray.append({'message': shortMessage, 'time': timeConvert(x.created_at).strftime("%d/%m/%y %H:%M:%S")})

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
                    embedArray.add_field(name="Date", value=f"> **Start**: " + timeConvert(dateStart).strftime("%d %B %Y, %I:%M:%S%p") + "\n> **End**: " + timeConvert(dateEnd).strftime("%d %B %Y, %I:%M:%S%p"), inline=False)
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
                                    deleted = await fetched.channel.purge(limit=3000, before=dateEnd, after=dateStart, check=checkUser)
                                    embed=discord.Embed(title=f'{len(deleted)} messages deleted from #{fetched.channel} in {fetched.guild}', color=0x00FF00)
                                    await progress.edit(embed=embed)
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
    
@client.command() #!timed        
async def timed(ctx):
    try:
        countdown = ctx.message.content.replace('!timed ', '')
        myList = countdown.split(' ')
        countdown = float(myList[0])

        myMessage = []
        remainder = countdown % 60
        hours = math.floor(countdown/60)
        minutes = math.floor(remainder)
        seconds = (remainder - math.floor(remainder)) * 60
        if hours > 1:
            myMessage.append(str(hours) + " hours")
        elif hours == 1:
            myMessage.append("1 hour")
        if minutes > 1:
            myMessage.append(str(minutes) + " minutes")
        elif minutes == 1:
            myMessage.append("1 minute")
        if seconds == 1:
            myMessage.append("1 second")
        elif seconds != 0:
            myMessage.append(str(int(seconds)) + " seconds")
            
        joinedMessage = " ".join(myMessage)
        msg = await ctx.reply(f'Message set to auto-delete in {joinedMessage}.')
        
    except:
        countdown = 5
        msg = await ctx.reply(f'Syntax error! Defaulting to auto-deletion in 5 minutes. Please use !timed # (# = minutes)')
    await asyncio.sleep(countdown * 60)
    await msg.delete()
    await ctx.message.delete()

@client.command() #!roll
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
    if '<@&423458739656458243>' in message.content and message.author.id != 1032276665092538489:
        reportChannel = client.get_channel(1033289784581427230)
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
    embed.set_footer(text=timeConvert(datetime.utcnow()).strftime("%d %B %Y, %I:%M:%S%p"))
    if message.attachments:
        embed.set_image(url=message.attachments[0].url)
    if report.children[1].value != "":
        additionalInfo = report.children[1].value
    else:
        additionalInfo = 'N/A'
    embed.add_field(name="Additional Info", value=additionalInfo, inline=False)
    reportChannel = client.get_channel(1033289784581427230)
    await reportChannel.send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) == '⭐':
        channel = client.get_channel(payload.channel_id)
        myMessage = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(myMessage.reactions, emoji='⭐')
        if (channel.id == 407561378564407297 or channel.id == 407561306162331674) and reaction.count >= 5:
            starChannel = client.get_channel(1032702775022321735)
            found = 0
            async for message in starChannel.history(limit=None):
                if message.embeds and message.embeds[0].footer and f'Message ID: {myMessage.id}' in message.embeds[0].footer.text:
                    found = 1
                    await message.edit(content='** **' + '⭐' * reaction.count)
                    break
            if found == 0:
                embed=discord.Embed(description=f'{reaction.message.content}\n\n> [\[Link\]]({reaction.message.jump_url})', color=0x14AB49)
                embed.set_footer(text=f'brought to you by degens at #{reaction.message.channel} | Message ID: {myMessage.id}')
                embed.set_author(name=f'{reaction.message.author.display_name}', icon_url=reaction.message.author.display_avatar)
                if reaction.message.attachments:
                    embed.set_image(url=reaction.message.attachments[0].url)
                await starChannel.send(content='** **' + '⭐' * reaction.count, embed=embed)

client.run(TOKEN)
