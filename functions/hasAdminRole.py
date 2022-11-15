import discord
from discord.ext import commands
import json
from .sql_start import sqlCursor

def hasAdminRole(ctx):
    if ctx.author.guild_permissions.administrator:
        return True

    sqlCursor.execute('SELECT adminRoles FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
    roleData = json.loads(sqlCursor.fetchone()[0])

    for role in ctx.author.roles:
        if role.id in roleData:
            return True
    return False