import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import json
from functions import *
import asyncio

docs = {

    "aliases":['embedrole'],

    "usage":"!embedroles",

    "description":"Specify user roles which will have access to Server Lizard's `!embed` command.\n\nRoles with admin permission do not require embed permission to use `!embed`.\n\nThis will not affect a role's Discord permissions.\n\nThe server administrator will always have embed access regardless of role.",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command(aliases=['embedrole'])
    @commands.max_concurrency(number=1, per=commands.BucketType.user, wait=False)
    async def embedroles(ctx):
        if not hasAdminRole(ctx) and not checkOwner(ctx):
            await ctx.reply("You do not have permission to use this command!", delete_after=20)
            return
            
        sqlCursor.execute('SELECT embedRoles FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
        roleData = json.loads(sqlCursor.fetchone()[0])

        roleList = []
        for role in roleData:
            roleList.append(f'- {ctx.guild.get_role(role)}')

        view = discord.ui.View()
        button1 = discord.ui.Button(label="Add", style=ButtonStyle.green, custom_id='add')
        button2 = discord.ui.Button(label="Remove", style=ButtonStyle.red, custom_id='remove')
        button3 = discord.ui.Button(label="Done", style=ButtonStyle.gray, custom_id='done')
        view.add_item(button1)
        if len(roleList) != 0:
            view.add_item(button2)
            content = '\n'.join(roleList)
        else:
            content = "No embed roles have been set"
        view.add_item(button3)

        msg1 = await ctx.send(embed=discord.Embed(title=f'**Embed roles for {ctx.guild.name}**', description=content), view=view)

        def checkButton(m):
            return m.message == msg1 and m.user == ctx.author
        try:
            interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
        except asyncio.TimeoutError:
            await msg1.edit(content='Timed out!', view=None)
        else:
            await interacted.response.defer()
            
            if interacted.data['custom_id'] == 'done':
                await msg1.edit(view=None)
                return
            elif interacted.data['custom_id'] == 'add':
                allRoleOptions = list(filter(lambda data: data.id not in roleData, ctx.guild.roles))
                if len(allRoleOptions) == 0:
                    await ctx.send(embed=discord.Embed(title='There are no more roles left to add!'))
                    return
                else:
                    options = list(map(lambda data: discord.SelectOption(label=f'{data[1].name}', value=f'{data[0]}') , list(enumerate(allRoleOptions, start=1))))
                    optionStart = 0
                    while True:
                        showOptions = options[optionStart:optionStart+22]
                        if optionStart != 0:
                            showOptions.append(discord.SelectOption(emoji='⬅️', label=f'Previous', value=f'previous'))
                        if len(options) - optionStart > 22:
                            showOptions.append(discord.SelectOption(emoji='➡️', label=f'Next', value=f'next'))
                        showOptions.append(discord.SelectOption(emoji='❌', label=f'Cancel', value=f'cancel'))

                        view = discord.ui.View()
                        myMenu = discord.ui.Select(placeholder="Select a role to add", options=showOptions)
                        view.add_item(myMenu)
                        await msg1.edit(view=view)

                        try:
                            interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                        except asyncio.TimeoutError:
                            await msg1.edit(content='Timed out!', view=None)
                            return
                        await interacted.response.defer()
                        if interacted.data["values"][0] == 'cancel':
                            await msg1.edit(embed=discord.Embed(title="Cancelled"), view=None)
                            return
                        elif interacted.data["values"][0] == 'next':
                            optionStart += 22
                        elif interacted.data["values"][0] == 'previous':
                            optionStart -= 22
                            if optionStart < 0:
                                optionStart = 0
                        else:
                            roleSelected = allRoleOptions[int(interacted.data["values"][0]) - 1]
                            break

                    roleData.append(roleSelected.id)
                    sql = 'UPDATE serverDB SET embedRoles = %s WHERE serverId = %s'
                    val = (json.dumps(roleData), ctx.guild.id)
                    sqlCursor.execute(sql, val)
                    sqlDb.commit()

                    embed=discord.Embed(title=f'`{roleSelected.name}` added as an embed role')
                    await msg1.edit(embed=embed, view=None)

            elif interacted.data['custom_id'] == 'remove':
                allRoleOptions = list(map(lambda data: discord.SelectOption(label=f'{ctx.guild.get_role(data[1]).name}', value=f'{data[0]}') , list(enumerate(roleData, start=1))))
                optionStart = 0
                while True:
                    showOptions = allRoleOptions[optionStart:optionStart+22]
                    if optionStart != 0:
                        showOptions.append(discord.SelectOption(emoji='⬅️', label=f'Previous', value=f'previous'))
                    if len(allRoleOptions) - optionStart > 22:
                        showOptions.append(discord.SelectOption(emoji='➡️', label=f'Next', value=f'next'))
                    showOptions.append(discord.SelectOption(emoji='❌', label=f'Cancel', value=f'cancel'))

                    view = discord.ui.View()
                    myMenu = discord.ui.Select(placeholder="Select a role to remove", options=showOptions)
                    view.add_item(myMenu)
                    await msg1.edit(view=view)

                    try:
                        interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                    except asyncio.TimeoutError:
                        await msg1.edit(content='Timed out!', view=None)
                        return
                    await interacted.response.defer()
                    if interacted.data["values"][0] == 'cancel':
                        await msg1.edit(embed=discord.Embed(title="Cancelled"), view=None)
                        return
                    elif interacted.data["values"][0] == 'next':
                        optionStart += 22
                    elif interacted.data["values"][0] == 'previous':
                        optionStart -= 22
                        if optionStart < 0:
                            optionStart = 0
                    else:
                        roleSelected = int(interacted.data["values"][0]) - 1
                        break

                removedRole = ctx.guild.get_role(roleData[roleSelected]).name
                roleData.pop(roleSelected)

                sql = 'UPDATE serverDB SET embedRoles = %s WHERE serverId = %s'
                val = (json.dumps(roleData), ctx.guild.id)
                sqlCursor.execute(sql, val)
                sqlDb.commit()

                embed=discord.Embed(title=f'`{removedRole}` removed as an embed role')
                await msg1.edit(embed=embed, view=None)