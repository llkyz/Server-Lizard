import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import json
from functions import *
import asyncio

docs = {

    "aliases":['adminrole'],

    "usage":"!adminroles, !adminroles add, !adminroles remove",

    "description":"Specify user roles which will have access to Server Lizard's admin commands.\n\n`!adminroles` or `!adminroles show` will show a list of roles with access to admin commands.\nSpecify new roles with `!adminroles add`, and remove them with `!adminroles remove`.\n\nThis will not affect a role's Discord permissions.\n\nThe server administrator will always have admin access regardless of role.",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command(aliases=['adminrole']) #!admin
    async def adminroles(ctx):
        if hasAdminRole(ctx) or checkOwner(ctx):

            sqlCursor.execute('SELECT adminRoles FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
            roleData = json.loads(sqlCursor.fetchone()[0])

            msgData = ctx.message.content.split(" ")

            #############################
            ### !adminroles / !adminroles show
            ################c#############
            if len(msgData) == 1 or msgData[1].lower() == "show":
                if roleData == None:
                    await ctx.send(embed=discord.Embed(title=f'There are currently no admin roles'))
                else:
                    roleList = []
                    for role in roleData:
                        roleList.append(f'- {ctx.guild.get_role(role)}')

                    await ctx.send(embed=discord.Embed(title=f'**Admin roles for {ctx.guild.name}**', description='\n'.join(roleList)))

            #############################
            ### !adminroles add
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
                                await ctx.send(embed=discord.Embed(title=f'{newRoleName} is already an admin role'))

                            else:
                                view = discord.ui.View()
                                button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                                button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                                view.add_item(item=button1)
                                view.add_item(item=button2)
                                embed=discord.Embed(title=f'Add `@{newRoleName}` as an admin role?')
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
                                        embed=discord.Embed(title=f'AdminRole Add cancelled')
                                        await ctx.send(embed=embed)

                                    elif interacted.data['custom_id'] == 'confirm':
                                        roleData.append(newRoleId)
                                        sql = 'UPDATE serverDB SET adminRoles = %s WHERE serverId = %s'
                                        val = (json.dumps(roleData), ctx.guild.id)
                                        sqlCursor.execute(sql, val)
                                        sqlDb.commit()

                                        embed=discord.Embed(title=f'`@{newRoleName}` added as an admin role')
                                        await ctx.send(embed=embed)

                        else:
                            await ctx.send(embed=discord.Embed(title=f'Invalid role entered'))

                #############################
                ### !adminroles remove
                #############################
                elif msgData[1].lower() == "remove":
                    if roleData == None:
                        await ctx.send(embed=discord.Embed(title=f'There are currently no admin roles'))

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
                                    embed=discord.Embed(title=f'Remove `@{removeRoleName}` as an admin role?')
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
                                            embed=discord.Embed(title=f'AdminRole Remove cancelled')
                                            await ctx.send(embed=embed)

                                        elif interacted.data['custom_id'] == 'confirm':
                                            roleData.pop(removeRoleIndex)
                                            sql = 'UPDATE serverDB SET adminRoles = %s WHERE serverId = %s'
                                            val = (json.dumps(roleData), ctx.guild.id)
                                            sqlCursor.execute(sql, val)
                                            sqlDb.commit()

                                            embed=discord.Embed(title=f'`@{removeRoleName}` removed as an admin role')
                                            await ctx.send(embed=embed)

                                else:
                                    await ctx.send(embed=discord.Embed(title=f'Invalid number entered'), delete_after=20)
                else:
                    await ctx.reply("Please use the following format: !adminroles / !adminroles add / !adminroles remove", delete_after=20)

        else:
            await ctx.reply("You do not have permission to use this command!", delete_after=20)