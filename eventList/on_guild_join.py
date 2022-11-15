import discord
from discord.ext import commands
import json
from functions import *

def setup(client):
    @client.event
    async def on_guild_join(guild):
        channel = guild.system_channel #getting system channel
        if channel.permissions_for(guild.me).send_messages: #making sure you have permissions
            await channel.send("🦎 **|** Server Lizard is here! Please use `!commands` to see a list of my commands.")


        sqlCursor.execute('SELECT * FROM serverDB WHERE serverId = %s', (guild.id,))
        userData = sqlCursor.fetchone()
        if userData == None:
            adminList = []
            for role in guild.roles:
                if role.permissions.administrator or role.permissions.manage_guild:
                    adminList.append(role.id)

            sql = "INSERT INTO serverDB (serverId, serverName, adminRoles, embedRoles) VALUES (%s, %s, %s, %s)"
            val = (guild.id, guild.name, json.dumps(adminList), json.dumps(adminList))
            sqlCursor.execute(sql, val)
            sqlDb.commit()
            print(f'Server data added for {guild.name}(id: {guild.id}')
        else:
            print(f'Server data already exists for {guild.name}(id: {guild.id}')