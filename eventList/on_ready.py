from apscheduler.schedulers.asyncio import AsyncIOScheduler
import discord
from discord.ext import commands
import asyncio
from functions import *

def setup(client):
    @client.event
    async def on_ready():
        async def checkFunc():
            await timedCheck(client)

        async def announcementFunc():
            await announcementCheck(client)

        scheduler = AsyncIOScheduler()
        scheduler.add_job(checkFunc, 'interval', minutes=1)
        scheduler.add_job(announcementFunc, 'interval', minutes=60)
        scheduler.start()
        print("Timed checker initialized")

        sqlCursor.execute('SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME = \'botSettings\'', (os.getenv('SQL_DATABASE'),))
        data = sqlCursor.fetchall()
        headerList = list(map(lambda x: x[3], data))
        sqlCursor.execute('SELECT * FROM botSettings')
        settings = sqlCursor.fetchone()

        settingsList = {}
        for x in range(len(headerList)):
            settingsList[headerList[x]] = settings[x]
        client.settings = settingsList

        print(f'{client.user} is connected to the following guilds:\n')
        for guild in client.guilds:
            print(f'{guild.name} (id: {guild.id})')

        await asyncio.sleep(5)
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name="!commands"))