import discord
from discord.ext import commands
from functions import *
import asyncio
from discord import Button, ButtonStyle

docs = {

    "aliases":['saverole'],

    "usage":"!saveroles",

    "description":"When a user leaves your server, their user roles are typically lost and will not be reassigned if they rejoin your server. If a user rejoins your server, this feature will send a message containing a list of their previous roles to the designated \"Save Role\" channel for easy reference.\n\nThis feature utilises role data saved in users' profile entries in the user profile channel. It requires user profiles (`!userprofiles`) to be first enabled and generated.\n\nOnce a channel is set, this feature will automatically activate. Undesignating a channel will also disable this feature.",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command(aliases=['saverole'])
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
    async def saveroles(ctx):
        if hasAdminRole(ctx) or checkOwner(ctx):
            sqlCursor.execute('SELECT saveRoleChannel FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
            channelData = sqlCursor.fetchone()[0]

            view = discord.ui.View()
            button1 = discord.ui.Button(label="Set", style=ButtonStyle.green, custom_id='add')
            button2 = discord.ui.Button(label="Remove", style=ButtonStyle.red, custom_id='remove')
            button3 = discord.ui.Button(label="Done", style=ButtonStyle.gray, custom_id='done')
            view.add_item(item=button1)
            if channelData == None:
                content = 'No Save Role channel has been set'
                content2 = 'Please set a channel to enable the Role Saving feature.'
            else:
                view.add_item(item=button2)
                content = f'`#{ctx.guild.get_channel(channelData)}` is currently set as the Save Role channel.'
                content2 = 'Use `SET` to overwrite this channel, or `REMOVE` to remove the channel and disable this feature.'
            view.add_item(item=button3)

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
                            sql = 'UPDATE serverDB SET saveRoleChannel = %s WHERE serverId = %s'
                            val = (optionSelected, ctx.guild.id)
                            sqlCursor.execute(sql, val)
                            sqlDb.commit()

                            await ctx.send(embed=discord.Embed(title=f'#{client.get_channel(optionSelected).name} set as Save Role channel.'))

                elif interacted.data['custom_id'] == 'remove':
                    sql = 'UPDATE serverDB SET saveRoleChannel = %s WHERE serverId = %s'
                    val = (None, ctx.guild.id)
                    sqlCursor.execute(sql, val)
                    sqlDb.commit()

                    embed=discord.Embed(title=f'`#{ctx.guild.get_channel(channelData)}` removed as the Save Role channel')
                    await ctx.send(embed=embed)
        else:
            await ctx.reply("You do not have permission to use this command!", delete_after=20)