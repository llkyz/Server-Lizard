import discord
from discord.ext import commands
from functions import *
import json
import asyncio
from discord import Button, ButtonStyle

docs = {

    "aliases":['adminpings'],

    "usage":"!adminping",

    "description":"If a user pings/mentions an admin role, this feature will send a message to the designated channel that links to the ping/mention. This allows for easier ping tracking instead of searching through an entire channel to find the ping.\n\nOnce a channel is set, this feature will automatically activate. Undesignating a channel will also disable this feature.",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command(aliases=['adminpings'])
    async def adminping(ctx):
        if not hasAdminRole(ctx) and checkOwner(ctx):
            await ctx.reply("You do not have permission to use this command!", delete_after=20)
            return

        sqlCursor.execute('SELECT adminPingChannel FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
        channelData = sqlCursor.fetchone()[0]

        view = discord.ui.View()
        button1 = discord.ui.Button(label="Set", style=ButtonStyle.green, custom_id='add')
        button2 = discord.ui.Button(label="Remove", style=ButtonStyle.red, custom_id='remove')
        button3 = discord.ui.Button(label="Done", style=ButtonStyle.gray, custom_id='done')
        view.add_item(button1)
        if channelData == None:
            content = 'No Admin Ping channel has been set'
            content2 = 'Please set a channel to enable the Admin Ping feature.'
        else:
            view.add_item(button2)
            content = f'`#{ctx.guild.get_channel(channelData)}` is currently set as the Admin Ping channel.'
            content2 = 'Use `SET` to overwrite this channel, or `REMOVE` to remove the channel and disable this feature.'
        view.add_item(button3)

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
                        sql = 'UPDATE serverDB SET adminPingChannel = %s WHERE serverId = %s'
                        val = (optionSelected, ctx.guild.id)
                        sqlCursor.execute(sql, val)
                        sqlDb.commit()

                        await ctx.send(embed=discord.Embed(title=f'#{client.get_channel(optionSelected).name} set as Admin Ping channel.'))

            elif interacted.data['custom_id'] == 'remove':
                sql = 'UPDATE serverDB SET adminPingChannel = %s WHERE serverId = %s'
                val = (None, ctx.guild.id)
                sqlCursor.execute(sql, val)
                sqlDb.commit()

                embed=discord.Embed(title=f'`#{ctx.guild.get_channel(channelData)}` removed as the Admin Ping channel')
                await ctx.send(embed=embed)