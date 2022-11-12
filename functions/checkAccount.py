import discord
from discord.ext import commands
from .sql_start import sqlCursor, sqlDb

async def checkAccount(ctx):
    sqlCursor.execute('SELECT * FROM userDB WHERE userId = %s', (ctx.author.id,))
    userData = sqlCursor.fetchone()
    if userData == None:
        sql = "INSERT INTO userDB (userId, coins, daily) VALUES (%s, %s, %s)"
        val = (ctx.author.id, 0, "0")
        sqlCursor.execute(sql, val)
        sqlDb.commit()
        await ctx.reply(f'Welcome {ctx.author.display_name}! Your account has been created.')
    else:
        return {'id': userData[0], 'money': userData[1], 'daily': userData[2]}