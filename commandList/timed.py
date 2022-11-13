import discord
from discord.ext import commands
import asyncio
import math

def setup(client):
    @client.command() #!timed        
    async def timed(ctx):
        try:
            msgData = ctx.message.content.replace("\n", " ").split(" ")
            countdown = float(msgData[1])
            
            if countdown <= 0:
                countdown = 5
                msg = await ctx.reply(f'Syntax error! Defaulting to auto-deletion in 5 minutes. Please use `!timed [minutes]`')
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
                msg = await ctx.reply(f'Message set to auto-delete in {joinedMessage}.')
            
        except Exception as e:
            print(e)
            countdown = 5
            msg = await ctx.reply(f'Syntax error! Defaulting to auto-deletion in 5 minutes. Please use `!timed [minutes]`')
        await asyncio.sleep(countdown * 60)
        await msg.delete()
        await ctx.message.delete()
