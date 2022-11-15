import discord
from discord.ext import commands
import json
from .sql_start import sqlCursor

def hasEmbedRole(ctx):
    sqlCursor.execute('SELECT embedRoles FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
    roleData = json.loads(sqlCursor.fetchone()[0])

    for role in ctx.author.roles:
        if role.id in roleData:
            return True
    return False