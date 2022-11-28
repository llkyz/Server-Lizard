import discord
from discord.ext import commands
from .sql_start import sqlCursor, sqlDb

def updateCoins(userData, result, bet):
    if result != 'tie':
        if result == 'win':
            val = (userData["coins"]+bet, userData["userId"])
        else:
            val = (userData["coins"]-bet, userData["userId"])
        sql = 'UPDATE userDB SET coins = %s WHERE userId = %s'
        sqlCursor.execute(sql, val)
        sqlDb.commit()