import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import asyncio
from datetime import datetime
import datetime
from functions import *

docs = {

    "aliases":['announcements'],

    "usage":"!announcement",

    "description":"Create announcement messages that constantly recur at a specificed interval",

    "category":"admin-features"
    
    }

def setup(client):
    @client.command(aliases=['announcements', 'anc']) #!battle
    async def announcement(ctx):
        if not hasAdminRole(ctx) and not checkOwner(ctx):
            await ctx.send(embed=discord.Embed(title=f'You do not have permission to use that command'), delete_after=20)
            return

        intervalOptions = {'1': 'Every hour', '6': 'Every 6 hours', '12': 'Every 12 hours', '24': 'Every day', '48': 'Every 2 days', '72': 'Every 3 days', '96': 'Every 4 days', '120': 'Every 5 days', '144': 'Every 6 days', '168': 'Every week', '336': 'Every 2 weeks', '504': 'Every 3 weeks', '672': 'Every month'}

        sqlCursor.execute('SELECT * FROM announcements WHERE guildId = %s', (ctx.guild.id,))
        announcementList = sqlCursor.fetchall()

        if len(announcementList) == 0:
            announcementListText = 'No announcements found'
        else:
            announcementListText = ""
            for x in announcementList:
                channelName = ctx.guild.get_channel(x[1])
                if x[2] == 0:
                    interval = "No"
                else:
                    interval = intervalOptions[str(x[2])]
                triggerTime = datetime.datetime(x[3], x[4], x[5], x[6]).strftime("%d %B %Y, %H:%M")
                announcementListText += f'**[#{channelName}]** {triggerTime}\nRepeat: {interval}\n\n'

        embed = discord.Embed(title="Scheduled announcements for this server", description=announcementListText)
        view = discord.ui.View()
        button1 = discord.ui.Button(label="Add", style=ButtonStyle.green, custom_id='add')
        button2 = discord.ui.Button(label="Remove", style=ButtonStyle.red, custom_id='remove')
        button3 = discord.ui.Button(label="View", style=ButtonStyle.blurple, custom_id='view')
        button4 = discord.ui.Button(label="Done", style=ButtonStyle.gray, custom_id='done')
        view.add_item(button1)
        if len(announcementList) != 0:
            view.add_item(button2)
            view.add_item(button3)
        view.add_item(button4)
        msg1 = await ctx.reply(embed=embed, view=view)

        def checkButton(m):
            return m.message == msg1 and m.user == ctx.author
        try:
            interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
        except asyncio.TimeoutError:
            await msg1.edit(content='Timed out!', view=None)
            return
       
        await interacted.response.defer()

        if interacted.data['custom_id'] == 'done':
            await msg1.edit(view=None)
            return
        elif interacted.data['custom_id'] == 'add':
            def makeOptions(myList):
                return discord.SelectOption(label=f'#{myList[1][0]}', value=f'{myList[1][1]}')
            options = list(map(makeOptions, list(enumerate(list(map(lambda data: (data.name, data.id) ,ctx.guild.text_channels)), start=1))))
            options.append(discord.SelectOption(label=f'Cancel', value=f'0'))
            view = discord.ui.View()
            myMenu = discord.ui.Select(placeholder="Choose a channel to send", options=options)
            view.add_item(myMenu)
            embed = discord.Embed(title="Adding new announcement")
            await msg1.edit(embed=embed, view=view)

            def checkButton(m):
                return m.message == msg1 and m.user == ctx.author
            try:
                interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
            except asyncio.TimeoutError:
                await msg1.edit(content='Timed out!', view=None)
                return
            
            await interacted.response.defer()
            channelId = int(interacted.data["values"][0])
            if channelId == 0:
                await msg1.edit(embed=discord.Embed(title="Cancelled"), view=None)
                return
            channelName = ctx.guild.get_channel(channelId)

            await msg1.edit(embed=discord.Embed(title=f'Adding announcement to {channelName}', description='Please enter the announcement date in the following format: dd-mm-yyyy'), view=None)

            def checkDate(m):
                return m.author == ctx.author and m.channel == ctx.channel
            
            try:
                interacted = await client.wait_for('message', timeout=300, check=checkDate)
            except asyncio.TimeoutError:
                await msg1.edit(content='Timed out!', view=None)
                return

            splitDate = interacted.content.split('-')
            await interacted.delete()
            try:
                year = int(splitDate[2])
                month = int(splitDate[1])
                day = int(splitDate[0])
                myDate = datetime.datetime(year, month, day)
            except Exception as e:
                print(e)
                await interacted.reply("Invalid date")
                return
            
            if myDate.date() < datetime.datetime.now().date():
                await interacted.reply("Cannot set a date before today!")
                return

            await msg1.edit(embed=discord.Embed(title=f'Creating announcement on #{channelName}\nDate: {myDate.date().strftime("%d %B %Y")}', description='Please enter the hour in 24-hour format (UTC time): 0 to 23'))

            try:
                interacted = await client.wait_for('message', timeout=300, check=checkDate)
            except asyncio.TimeoutError:
                await msg1.edit(content='Timed out!')
                return
            
            if not(interacted.content.isnumeric() and int(interacted.content) >= 0 and int(interacted.content) <= 23):
                await interacted.reply("Invalid number")
                return
            hour = int(interacted.content)
            myDate = myDate.replace(hour=hour)
            await interacted.delete()

            view = discord.ui.View()
            button1 = discord.ui.Button(label="Yes", style=ButtonStyle.green, custom_id='yes')
            button2 = discord.ui.Button(label="No", style=ButtonStyle.red, custom_id='no')
            view.add_item(button1)
            view.add_item(button2)
            await msg1.edit(embed=discord.Embed(title=f'Creating announcement on #{channelName}\nDate: {myDate.strftime("%d %B %Y, %H:%M")}', description='Do you want this announcement to repeat at regular intervals?'), view=view)
            
            try:
                interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
            except asyncio.TimeoutError:
                await msg1.edit(content='Timed out!', view=None)

            await msg1.edit(view=None)
            if interacted.data['custom_id'] == 'yes':
                await interacted.response.defer()
                options = []
                for x in intervalOptions:
                    options.append(discord.SelectOption(label=intervalOptions[x], value=x))
                view = discord.ui.View()
                myMenu = discord.ui.Select(placeholder="Select an interval", options=options)
                view.add_item(myMenu)
                await msg1.edit(embed=discord.Embed(title=f'Creating announcement on #{channelName}\nDate: {myDate.strftime("%d %B %Y, %H:%M")}', description='Select an interval to repeat the announcement'), view=view)

                def checkButton(m):
                    return m.message == msg1 and m.user == ctx.author
                try:
                    interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                except asyncio.TimeoutError:
                    await msg1.edit(content='Timed out!', view=None)
                    return

                await msg1.edit(view=None)
                interval = int(interacted.data["values"][0])

            elif interacted.data['custom_id'] == 'no':
                interval = 0
                
            myModal = AnnouncementModal(title="Announcement Form")
            await interacted.response.send_modal(myModal)
            await myModal.wait()

            embed = discord.Embed(title=f'Creating announcement on #{channelName}\nDate: {myDate.strftime("%d %B %Y, %H:%M")}\nRepeat: {"No" if interval == 0 else intervalOptions[str(interval)]}', description=myModal.children[0].value)
            await msg1.edit(embed=embed)
            view = discord.ui.View()
            button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
            button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
            view.add_item(button1)
            view.add_item(button2)
            msg1 = await ctx.send(embed=discord.Embed(title='Create this announcement?'), view=view)

            try:
                interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
            except asyncio.TimeoutError:
                await msg1.edit(content='Timed out!', view=None)
                return

            await interacted.response.defer()

            if interacted.data['custom_id'] == 'confirm':
                sql = "INSERT INTO announcements (guildId, channelId, waitTime, year, month, day, hour, message) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (ctx.guild.id, channelId, interval, year, month, day, hour, myModal.children[0].value)
                sqlCursor.execute(sql, val)
                sqlDb.commit()

                await msg1.edit(embed=discord.Embed(title='Announcement scheduled'), view=None)
            elif interacted.data['custom_id'] == 'cancel':
                await msg1.edit(embed=discord.Embed(title='Announcement cancelled'), view=None)
                return

        elif interacted.data['custom_id'] == 'view':
            options = []
            counter = 1
            for x in announcementList:
                channelName = ctx.guild.get_channel(x[1])
                options.append(discord.SelectOption(label=f'#{channelName}', value=f'{str(counter)}'))
                counter += 1
            options.append(discord.SelectOption(label=f'Cancel', value=f'0'))
            view = discord.ui.View()
            myMenu = discord.ui.Select(placeholder="Select an announcement", options=options)
            view.add_item(myMenu)
            await msg1.edit(view=view)

            def checkButton(m):
                return m.message == msg1 and m.user == ctx.author
            try:
                interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
            except asyncio.TimeoutError:
                await msg1.edit(content='Timed out!', view=None)
                return
            
            await interacted.response.defer()
            announcementIndex = int(interacted.data["values"][0]) - 1
            if announcementIndex == -1:
                await msg1.edit(view=None)
                return
            y = announcementList[announcementIndex]
            embed = discord.Embed(title=f'[#{ctx.guild.get_channel(y[1])}]\nAnnouncement Date: {datetime.datetime(y[3], y[4], y[5], y[6]).strftime("%d %B %Y, %H:%M")}\nRepeat: {intervalOptions[str(y[2])] if y[2] else "No"}', description=f'{y[7]}')
            await msg1.edit(embed=embed, view=None)
            return

        elif interacted.data['custom_id'] == 'remove':
            options = []
            counter = 1
            for x in announcementList:
                channelName = ctx.guild.get_channel(x[1])
                options.append(discord.SelectOption(label=f'#{channelName}', value=f'{str(counter)}'))
                counter += 1
            options.append(discord.SelectOption(label=f'Cancel', value=f'0'))
            view = discord.ui.View()
            myMenu = discord.ui.Select(placeholder="Select an announcement", options=options)
            view.add_item(myMenu)
            await msg1.edit(view=view)

            def checkButton(m):
                return m.message == msg1 and m.user == ctx.author
            try:
                interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
            except asyncio.TimeoutError:
                await msg1.edit(content='Timed out!', view=None)
                return
            
            await interacted.response.defer()
            announcementIndex = int(interacted.data["values"][0]) - 1
            if announcementIndex == -1:
                await msg1.edit(view=None)
                return
            y = announcementList[announcementIndex]
            embed = discord.Embed(title=f'[#{ctx.guild.get_channel(y[1])}]\nAnnouncement Date: {datetime.datetime(y[3], y[4], y[5], y[6]).strftime("%d %B %Y, %H:%M")}\nRepeat: {intervalOptions[str(y[2])] if y[2] else "No"}', description=f'{y[7]}')
            await msg1.edit(embed=embed, view=None)
            view = discord.ui.View()
            button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
            button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
            view.add_item(button1)
            view.add_item(button2)
            msg1 = await ctx.send(embed=discord.Embed(title="Delete this announcement?"), view=view)

            try:
                interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
            except asyncio.TimeoutError:
                await msg1.edit(content='Timed out!', view=None)
                return

            await interacted.response.defer()

            if interacted.data['custom_id'] == 'confirm':
                sqlCursor.execute('DELETE FROM announcements WHERE guildId = %s AND channelId = %s AND waitTime = %s AND year = %s AND month = %s AND day = %s AND hour = %s AND message = %s', (y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7]))
                sqlDb.commit()
                await msg1.edit(embed=discord.Embed(title="Announcement deleted"), view=None)
                return
            elif interacted.data['custom_id'] == 'cancel':
                await msg1.edit(embed=discord.Embed(title="Cancelled"), view=None)
                return

    class AnnouncementModal(discord.ui.Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.add_item(discord.ui.InputText(label="Write your announcement here", style=discord.InputTextStyle.long))

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.defer()