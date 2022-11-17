import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import json
from functions import *
import asyncio

docs = {

    "aliases":['embedrole'],

    "usage":"!embedroles show, !embedroles add, !embedroles remove",

    "description":"Specify user roles which will have access to Server Lizard's `!embed` command.\n\n`!embedroles` or `!embedroles show` will show a list of roles with access to the embed command.\nSpecify new roles with `!embedroles add`, and remove them with `!embedroles remove`.\n\nThis will not affect a role's Discord permissions.\n\nThe server administrator will always have embed access regardless of role.",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command(aliases=['embedrole']) #!admin
    async def embedroles(ctx):
        if hasAdminRole(ctx) or checkOwner(ctx):

            sqlCursor.execute('SELECT embedRoles FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
            roleData = json.loads(sqlCursor.fetchone()[0])

            msgData = ctx.message.content.split(" ")

            #############################
            ### !embedroles / !embedroles show
            #############################
            if len(msgData) == 1 or msgData[1].lower() == "show":
                if roleData == None:
                    await ctx.send(embed=discord.Embed(title=f'There are currently no embed roles'))
                else:
                    roleList = []
                    for role in roleData:
                        roleList.append(f'- {ctx.guild.get_role(role)}')

                    await ctx.send(embed=discord.Embed(title=f'**Embed roles for {ctx.guild.name}**', description='\n'.join(roleList)))

            #############################
            ### !embedroles add
            #############################
            else:
                if msgData[1].lower() == "add":
                    msg1 = await ctx.send(embed=discord.Embed(title=f'Please ping/mention the role that you wish to add. (e.g. `@moderator`)'))

                    def check(m):
                        return m.channel == ctx.channel and m.author == ctx.author

                    try:
                        interacted = await client.wait_for('message', timeout=300, check=check)

                    except asyncio.TimeoutError:
                        await msg1.edit(content='Timed out!')

                    else:
                        if interacted.content[0:3] == "<@&" and interacted.content[-1] == ">":
                            newRoleId = int(interacted.content.replace("<@&","").replace(">",""))
                            newRoleName = ctx.guild.get_role(newRoleId)

                            if newRoleName == None:
                                await ctx.send(embed=discord.Embed(title=f'Invalid role entered'))

                            elif newRoleId in roleData:
                                await ctx.send(embed=discord.Embed(title=f'{newRoleName} is already an embed role'))

                            else:
                                view = discord.ui.View()
                                button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                                button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                                view.add_item(item=button1)
                                view.add_item(item=button2)
                                embed=discord.Embed(title=f'Add `@{newRoleName}` as an embed role?')
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
                                        embed=discord.Embed(title=f'EmbedRole Add cancelled')
                                        await ctx.send(embed=embed)

                                    elif interacted.data['custom_id'] == 'confirm':
                                        roleData.append(newRoleId)
                                        sql = 'UPDATE serverDB SET embedRoles = %s WHERE serverId = %s'
                                        val = (json.dumps(roleData), ctx.guild.id)
                                        sqlCursor.execute(sql, val)
                                        sqlDb.commit()

                                        embed=discord.Embed(title=f'`@{newRoleName}` added as an embed role')
                                        await ctx.send(embed=embed)

                        else:
                            await ctx.send(embed=discord.Embed(title=f'Invalid role entered'))

                #############################
                ### !embedroles remove
                #############################
                elif msgData[1].lower() == "remove":
                    if roleData == None:
                        await ctx.send(embed=discord.Embed(title=f'There are currently no embed roles'))

                    else:
                        roleList = []
                        for x in range(len(roleData)):
                            roleList.append(f'{x+1}. {ctx.guild.get_role(roleData[x])}')

                        msg1 = await ctx.send(embed=discord.Embed(title=f'Please enter the number for the role you wish to remove', description='\n'.join(roleList)))
                        
                        def check(m):
                            return m.channel == ctx.channel and m.author == ctx.author

                        try:
                            interacted = await client.wait_for('message', timeout=300, check=check)

                        except asyncio.TimeoutError:
                            await msg1.edit(content='Timed out!')

                        else:
                            try:
                                removeRoleIndex = int(interacted.content) - 1
                            except:
                                await ctx.send(embed=discord.Embed(title=f'Invalid input'))
                            else:
                                if interacted.content.isnumeric() and removeRoleIndex >= 0 and removeRoleIndex < len(msgData):
                                    removeRoleName = ctx.guild.get_role(roleData[removeRoleIndex])

                                    view = discord.ui.View()
                                    button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                                    button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                                    view.add_item(item=button1)
                                    view.add_item(item=button2)
                                    embed=discord.Embed(title=f'Remove `@{removeRoleName}` as an embed role?')
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
                                            embed=discord.Embed(title=f'EmbedRole Remove cancelled')
                                            await ctx.send(embed=embed)

                                        elif interacted.data['custom_id'] == 'confirm':
                                            roleData.pop(removeRoleIndex)
                                            sql = 'UPDATE serverDB SET embedRoles = %s WHERE serverId = %s'
                                            val = (json.dumps(roleData), ctx.guild.id)
                                            sqlCursor.execute(sql, val)
                                            sqlDb.commit()

                                            embed=discord.Embed(title=f'`@{removeRoleName}` removed as an embed role')
                                            await ctx.send(embed=embed)

                                else:
                                    await ctx.send(embed=discord.Embed(title=f'Invalid number entered'))
                else:
                    await ctx.send("Please use the following format: !embedroles / !embedroles add / !embedroles remove")

        else:
            await ctx.reply("You do not have permission to use this command!")