import discord
from discord.ext import commands
import asyncio
import math
from functions import *
from functions.sql_start import SQLObject
from datetime import datetime

docs = {

    "aliases":['timer', 'time'],

    "usage":"!timed [minutes]",

    "description":"Include this in your message to auto-delete it after a set amount of time. Works both with text messages and images.",

    "category":"messages"
    
    }

async def setup(client):
    @client.command(aliases=['timer', 'time'])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def timed(ctx):
        try:
            msgData = ctx.message.content.replace("\n", " ").split(" ")
            countdown = float(msgData[1])
            
            if countdown <= 0:
                countdown = 5
                await ctx.reply(f'Syntax error! Defaulting to auto-deletion in 5 minutes. Please use `!timed [minutes]`', delete_after=60)
            elif countdown > 10080:
                countdown = 10080
                await ctx.reply(f'That\'s beyond the maximum time limit! Auto-deletion has been set to 7 days.', delete_after=60)
            else:
                myMessage = []
                days = math.floor(countdown/1440)
                hours = math.floor(countdown/60 - (days * 24))
                remainder = countdown % 60
                minutes = math.floor(remainder)
                seconds = (remainder - math.floor(remainder)) * 60
                if days > 1:
                    myMessage.append(str(days) + " days")
                elif days == 1:
                    myMessage.append("1 day")
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
        SQLObject.execute(sql, val)
        SQLObject.commit()