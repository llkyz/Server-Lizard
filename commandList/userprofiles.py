import discord
from discord.ext import commands
from functions import *
import asyncio
from discord import Button, ButtonStyle

docs = {

    "aliases":['userprofile'],

    "usage":"!userprofiles",

    "description":"Designate a channel to store user profiles of all the members in your server. This feature is meant for server management and recording disciplinary actions.\n\nUse `!userprofiles set` to designate a channel. Once a channel is set, use `POPULATE` to generate user profiles. Use `!userprofiles remove` to undesignate the channel and disable this feature.\n\nA user profile channel must be set with user profiles generated in order to use the `!saveroles` and `!infraction` features.",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command(aliases=['userProfiles', 'userprofile', 'userProfile'])
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
    async def userprofiles(ctx):
        if hasAdminRole(ctx) or checkOwner(ctx):
            sqlCursor.execute('SELECT userProfilesChannel FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
            channelData = sqlCursor.fetchone()[0]

            view = discord.ui.View()
            button1 = discord.ui.Button(label="Set", style=ButtonStyle.green, custom_id='add')
            button2 = discord.ui.Button(label="Remove", style=ButtonStyle.red, custom_id='remove')
            button3 = discord.ui.Button(label="Populate", style=ButtonStyle.blurple, custom_id='populate')
            button4 = discord.ui.Button(label="Done", style=ButtonStyle.gray, custom_id='done')
            view.add_item(button1)
            if channelData == None:
                content = 'No User Profile channel has been set'
                content2 = 'Please set a channel to enable and generate User Profiles.'
            else:
                view.add_item(button2)
                view.add_item(button3)
                content = f'`#{ctx.guild.get_channel(channelData)}` is currently set as the User Profile channel.'
                content2 = 'Use `SET` to overwrite this channel, or `REMOVE` to remove the channel and disable this feature. Use `POPULATE` to generate user profiles in the User Profile channel.'
            view.add_item(button4)

            msg1 = await ctx.send(embed=discord.Embed(title=content, description=content2), view=view)

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
                    def makeOptions(myList):
                        return discord.SelectOption(label=f'#{myList[1][0]}', value=f'{myList[1][1]}')

                    options = list(map(makeOptions, list(enumerate(list(map(lambda data: (data.name, data.id) ,ctx.guild.text_channels)), start=1))))
                    options.append(discord.SelectOption(label=f'Cancel', value=f'0'))
                    view = discord.ui.View()
                    myMenu = discord.ui.Select(placeholder="Choose a channel to set", options=options)
                    view.add_item(myMenu)
                    msg2 = await ctx.send(view=view)

                    def checkButton(m):
                        return m.message == msg2 and m.user == ctx.author
                    try:
                        interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                    except asyncio.TimeoutError:
                        await msg2.edit(content='Timed out!', view=None)
                    else:
                        await interacted.response.defer()
                        optionSelected = int(interacted.data["values"][0])
                        await msg2.delete()

                        if optionSelected == 0:
                            await ctx.send(embed=discord.Embed(title="Set Channel cancelled"))
                        else:
                            sql = 'UPDATE serverDB SET userProfilesChannel = %s WHERE serverId = %s'
                            val = (optionSelected, ctx.guild.id)
                            sqlCursor.execute(sql, val)
                            sqlDb.commit()

                            await ctx.send(embed=discord.Embed(title=f'#{client.get_channel(optionSelected).name} set as User Profile channel.'))

                elif interacted.data['custom_id'] == 'remove':
                    sql = 'UPDATE serverDB SET userProfilesChannel = %s WHERE serverId = %s'
                    val = (None, ctx.guild.id)
                    sqlCursor.execute(sql, val)
                    sqlDb.commit()

                    embed=discord.Embed(title=f'`#{ctx.guild.get_channel(channelData)}` removed as the User Profile channel')
                    await ctx.send(embed=embed)

                elif interacted.data['custom_id'] == 'populate':
                    view = discord.ui.View()
                    button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                    button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                    view.add_item(item=button1)
                    view.add_item(item=button2)
                    embed=discord.Embed(title=f'Populate User Profile channel?', description=f'This will fill your selected channel with user profiles, and may take anywhere from a few minutes to a few hours depending on the size of your server. The message \"All done!\" will be sent upon completion.\n\n**>>WARNING<<** Do not run this command if your User Profile channel has already been populated.')
                    msg1 = await ctx.send(embed=embed, view=view)

                    def checkButton(m):
                        return m.message == msg1 and m.user == ctx.author

                    try:
                        interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                    except asyncio.TimeoutError:
                        view.clear_items()
                        await msg1.edit(content='Timed out!', view=view)
                    else:
                        await interacted.response.defer()
                        view.clear_items()
                        await msg1.edit(view=view)

                        if interacted.data['custom_id'] == 'cancel':
                            embed=discord.Embed(title=f'UserProfiles Populate cancelled')
                            await ctx.send(embed=embed)

                        elif interacted.data['custom_id'] == 'confirm':
                            msg2 = await ctx.send(embed=discord.Embed(title="Populating user profiles... sit tight!"))
                            channel = client.get_channel(channelData)
                            for member in channel.guild.members:
                                userName = member.name + "#" + member.discriminator
                                roleList = []
                                for x in member.roles:
                                    roleList.append(x.name)

                                embed = discord.Embed(title=f'{member.display_name} ({userName})', description=f'**User ID**: {member.id}\n**User Roles**: {roleList}\n**Infractions**:')
                                embed.set_thumbnail(url=member.display_avatar.url)
                                await channel.send(embed=embed)
                            await msg2.reply(embed=discord.Embed(title="All done!"))

        else:
            await ctx.reply("You do not have permission to use this command!", delete_after=20)