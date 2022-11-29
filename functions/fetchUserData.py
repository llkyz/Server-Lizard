import discord
from discord.ext import commands
from .sql_start import sqlCursor, sqlDb
import os

async def fetchUserData(user):
    sqlCursor.execute('SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME = \'userDB\'', (os.getenv('SQL_DATABASE'),))
    data = sqlCursor.fetchall()
    headerList = list(map(lambda x: x[3], data))

    sqlCursor.execute('SELECT * FROM userDB WHERE userId = %s', (user.id,))
    userData = sqlCursor.fetchone()
    if userData == None:
        sql = "INSERT INTO userDB (userId, userName, coins, daily) VALUES (%s, %s, %s, %s)"
        val = (user.id, user.name + "#" + user.discriminator, 0, "0")
        sqlCursor.execute(sql, val)
        sqlDb.commit()

        sqlCursor.execute('SELECT * FROM userDB WHERE userId = %s', (user.id,))
        userData = sqlCursor.fetchone()

    userInfo = {}
    for x in range(len(headerList)):
        userInfo[headerList[x]] = userData[x]
    return userInfo