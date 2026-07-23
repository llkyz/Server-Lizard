import discord
from discord.ext import commands
from functions.sql_start import SQLObject
from datetime import datetime, timedelta

async def announcementCheck(client):
    SQLObject.execute('SELECT * FROM announcements')
    announcementData = SQLObject.sqlCursor.fetchall()

    for x in announcementData:
        try:
            interval = x[2]
            scheduledTime = datetime(x[3], x[4], x[5], x[6])
            if int(scheduledTime.timestamp()) < int(datetime.now().timestamp()):
                guild = client.get_guild(x[0])
                channel = guild.get_channel(x[1])
                await channel.send(embed=discord.Embed(description=f'{x[7]}'))
                if interval == 0:
                    SQLObject.execute('DELETE FROM announcements WHERE guildId = %s AND channelId = %s AND waitTime = %s AND year = %s AND month = %s AND day = %s AND hour = %s AND message = %s', (x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]))
                    SQLObject.commit()
                else:
                    newTime = scheduledTime + timedelta(hours=interval)
                    year = newTime.year
                    month = newTime.month
                    day = newTime.day
                    hour = newTime.hour
                    sql = 'UPDATE announcements SET year = %s, month = %s, day = %s, hour = %s WHERE guildId = %s AND channelId = %s AND waitTime = %s AND year = %s AND month = %s AND day = %s AND hour = %s AND message = %s'
                    val = (year, month, day, hour, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])
                    SQLObject.execute(sql, val)
                    SQLObject.commit()
        except Exception as e:
            print(e)
            pass