import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import asyncio
import math

docs = {

    "aliases":['setReminder', 'remind'],

    "usage":"!reminder [minutes] [message]",

    "description":"Include this in your message to receive a reminder after a set amount of time. Works both with text messages and images.",

    "category":"messages"
    
    }

def setup(client):
    @client.command(aliases=['remind', 'setreminder'])
    async def reminder(ctx):
        try:
            msgData = ctx.message.content.replace("\n", " ").split(" ")
            countdown = float(msgData[1])
            
            if countdown <= 0:
                countdown = 5
                await ctx.reply(f'Syntax error! Defaulting to reminder in j5 minutes. Please use `!reminder [minutes] [message]`')
            elif countdown > 1440:
                countdown = 1440
                await ctx.reply(f'That\'s beyond the maximum time limit! Timer has been set to 24 hours.')
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
                await ctx.reply(f'Reminder set for {joinedMessage}.')
            
        except:
            countdown = 5
            await ctx.reply(f'Syntax error! Defaulting to reminder in 5 minutes. Please use `!reminder [minutes] [message]`')
        await asyncio.sleep(countdown * 60)

        view = discord.ui.View()
        button1 = discord.ui.Button(label="Source", style=ButtonStyle.gray, url=ctx.message.jump_url)
        view.add_item(button1)
        embed = discord.Embed(description=f'> {" ".join(msgData[2:])}')
        embed.set_author(name=f'[REMINDER!]', icon_url=ctx.author.display_avatar)
        await ctx.channel.send(content=f'{ctx.author.mention}', embed=embed, view=view)