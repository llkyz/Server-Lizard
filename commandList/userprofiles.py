import discord
from discord.ext import commands
from functions import *
import asyncio
from discord import Button, ButtonStyle

docs = {

    "aliases":['userprofile'],

    "usage":"!userprofiles set, !userprofiles remove",

    "description":"Placeholder",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command(aliases=['userprofile'])
    async def userprofiles(ctx):
        if hasAdminRole(ctx) or checkOwner(ctx):
            msgData = ctx.message.content.split(" ")
            
            sqlCursor.execute('SELECT userProfilesChannel FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
            channelData = sqlCursor.fetchone()[0]
            
            ##############################
            ### !userprofiles / !userprofiles show
            ##############################
            if len(msgData) == 1 or msgData[1].lower() == "show":
                if channelData == None:
                    await ctx.reply("No user profile channel has been set. Please use `!userprofiles set` to designate a User Profile channel", delete_after=20)
                else:
                    await ctx.reply(f'`#{ctx.guild.get_channel(channelData)}` has been set as the User Profile channel. Please use `!userprofile set` to overwrite the channel or `!userprofiles remove` to undesignate the channel', delete_after=20)


            ##############################
            ### !userprofiles set
            ##############################
            elif msgData[1].lower() == "set":
                if channelData != None:
                    await ctx.send(embed=discord.Embed(title=f'`#{ctx.guild.get_channel(channelData)}` is already set as the User Profile channel. Setting a new channel will overwrite the previous one'))
                msg1 = await ctx.send(embed=discord.Embed(title="Please ping/mention the channel you wish to designate (e.g. `#general`), or type `Cancel` to abort"))

                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author

                try:
                    interacted = await client.wait_for('message', timeout=300, check=check)

                except asyncio.TimeoutError:
                    await msg1.edit(content='Timed out!')

                else:
                    if interacted.content[0:2] == "<#" and interacted.content[-1] == ">":
                        newChannelId = int(interacted.content.replace("<#","").replace(">",""))
                        newChannelName = ctx.guild.get_channel(newChannelId)

                        if newChannelName == None:
                            await ctx.send(embed=discord.Embed(title=f'Invalid channel entered'))

                        else:
                            view = discord.ui.View()
                            button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                            button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                            view.add_item(item=button1)
                            view.add_item(item=button2)
                            embed=discord.Embed(title=f'Set `#{newChannelName}` as the User Profile channel?')
                            msg2 = await ctx.send(embed=embed, view=view)

                            def checkButton(m):
                                return m.message == msg2 and m.user == ctx.author

                            try:
                                interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                            except asyncio.TimeoutError:
                                view.clear_items()
                                await msg2.edit(content='Timed out!', view=view)
                            else:
                                await interacted.response.defer()
                                view.clear_items()
                                await msg2.edit(view=view)

                                if interacted.data['custom_id'] == 'cancel':
                                    embed=discord.Embed(title=f'UserProfiles Set cancelled')
                                    await ctx.send(embed=embed)

                                elif interacted.data['custom_id'] == 'confirm':
                                    sql = 'UPDATE serverDB SET userProfilesChannel = %s WHERE serverId = %s'
                                    val = (newChannelId, ctx.guild.id)
                                    sqlCursor.execute(sql, val)
                                    sqlDb.commit()

                                    embed=discord.Embed(title=f'`#{newChannelName}` set as the User Profile channel')
                                    await ctx.send(embed=embed)


                    elif interacted.content == "cancel" or interacted.content == "Cancel":
                        await ctx.send(embed=discord.Embed(title=f'UserProfile Set cancelled'))
                    else:
                        await ctx.send(embed=discord.Embed(title=f'Invalid channel entered'))

            ##############################
            ### !userprofiles remove
            ##############################
            elif msgData[1].lower() == "remove":
                if channelData == None:
                    await ctx.send(embed=discord.Embed(title="There is no User Profile channel set"))
                else:
                    view = discord.ui.View()
                    button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                    button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                    view.add_item(item=button1)
                    view.add_item(item=button2)
                    embed=discord.Embed(title=f'Remove `#{ctx.guild.get_channel(channelData)}` as the User Profile channel?')
                    msg2 = await ctx.send(embed=embed, view=view)

                    def checkButton(m):
                        return m.message == msg2 and m.user == ctx.author

                    try:
                        interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                    except asyncio.TimeoutError:
                        view.clear_items()
                        await msg2.edit(content='Timed out!', view=view)
                    else:
                        await interacted.response.defer()
                        view.clear_items()
                        await msg2.edit(view=view)

                        if interacted.data['custom_id'] == 'cancel':
                            embed=discord.Embed(title=f'UserProfiles Remove cancelled')
                            await ctx.send(embed=embed)

                        elif interacted.data['custom_id'] == 'confirm':
                            sql = 'UPDATE serverDB SET userProfilesChannel = %s WHERE serverId = %s'
                            val = (None, ctx.guild.id)
                            sqlCursor.execute(sql, val)
                            sqlDb.commit()

                            embed=discord.Embed(title=f'`#{ctx.guild.get_channel(channelData)}` removed as the User Profile channel')
                            await ctx.send(embed=embed)
            else:
                await ctx.reply("Please use `!userprofiles set` to designate a User Profile channel or `!userprofiles remove` to remove a designated channel", delete_after=20)
        else:
            await ctx.reply("You do not have permission to use this command!", delete_after=20)