import discord
from discord.ext import commands
from .sql_start import SQLObject
from datetime import datetime

async def timedCheck(client):
    SQLObject.execute('SELECT * FROM timedDB')
    timedData = SQLObject.fetchall()
    for x in timedData:
        # compares message's deleteTime and the current timestamp
        # if current timestamp is larger than the message deleteTime, then the message is deleted
        if x[2] < int(datetime.now().timestamp()):
            try:
                channel = await client.fetch_channel(x[1])
                message = await channel.fetch_message(x[0])
                await message.delete()
            except:
                print("Message can't be found")
            SQLObject.execute('DELETE FROM timedDB WHERE messageId = %s', (x[0],))
            SQLObject.commit()