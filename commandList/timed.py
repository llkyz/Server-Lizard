import discord
from discord.ext import commands
import asyncio
import math
from functions import *
from datetime import datetime

docs = {

    "aliases":['timer'],

    "usage":"!timed [minutes]",

    "description":"Include this in your message to auto-delete it after a set amount of time. Works both with text messages and images.",

    "category":"messages"
    
    }

def setup(client):
    @client.command(aliases=['timer'])
    async def timed(ctx):
        try:
            msgData = ctx.message.content.replace("\n", " ").split(" ")
            countdown = float(msgData[1])
            
            if countdown <= 0:
                countdown = 5
                await ctx.reply(f'Syntax error! Defaulting to auto-deletion in 5 minutes. Please use `!timed [minutes]`', delete_after=60)
            elif countdown > 1440:
                countdown = 1440
                await ctx.reply(f'That\'s beyond the maximum time limit! Auto-deletion has been set to 24 hours.', delete_after=60)
            else:
                myMessage = []
                remainder = countdown % 60
                hours = math.floor(countdown/60)
                minutes = math.floor(remainder)
                seconds = (remainder - math.floor(remainder)) * 60
                if hours > 1:
                    myMessage.append(str(hours) + " hours")
                elif hours == 1:
                    myMessage.append("1 hour")
                if minutes > 1:
                    myMessage.append(str(minutes) + " minutes")
                elif minutes == 1:
                    myMessage.append("1 minute")
                if seconds == 1:
                    myMessage.append("1 second")
                elif seconds != 0:
                    myMessage.append(str(int(seconds)) + " seconds")
                    
                joinedMessage = " ".join(myMessage)
                await ctx.reply(f'Message set to auto-delete in {joinedMessage}.', delete_after=60)
            
        except:
            countdown = 5
            await ctx.reply(f'Syntax error! Defaulting to auto-deletion in 5 minutes. Please use `!timed [minutes]`', delete_after=60)

        sql = "INSERT INTO timedDB (messageId, channelId, deleteTime) VALUES (%s, %s, %s)"
        val = (ctx.message.id, ctx.channel.id, int(datetime.now().timestamp()) + countdown*60)
        sqlCursor.execute(sql, val)
        sqlDb.commit()