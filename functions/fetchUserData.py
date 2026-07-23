import discord
from discord.ext import commands
from functions.sql_start import SQLObject
import os

async def fetchUserData(user):
    SQLObject.execute('SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME = \'userDB\'', (os.getenv('SQL_DATABASE'),))
    data = SQLObject.fetchall()
    headerList = list(map(lambda x: x[3], data))

    SQLObject.execute('SELECT * FROM userDB WHERE userId = %s', (user.id,))
    userData = SQLObject.fetchone()
    if userData == None:
        sql = "INSERT INTO userDB (userId, userName, coins, daily) VALUES (%s, %s, %s, %s)"
        val = (user.id, user.name + "#" + user.discriminator, 0, "0")
        SQLObject.execute(sql, val)
        SQLObject.commit()

        SQLObject.execute('SELECT * FROM userDB WHERE userId = %s', (user.id,))
        userData = SQLObject.sqlCursor.fetchone()

    userInfo = {}
    for x in range(len(headerList)):
        userInfo[headerList[x]] = userData[x]
    return userInfo