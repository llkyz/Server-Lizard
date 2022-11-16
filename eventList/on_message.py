import discord
from discord.ext import commands
import random
from functions import *
import json

def setup(client):
    @client.event
    async def on_message(message):
        if message.channel.type is discord.ChannelType.private:
            prefix = 'DM'
        else:
            prefix = str(message.guild) + " #" + str(message.channel)
            print(f"[{prefix}] " + str(message.author) + ": " + str(message.content))

            if '<@1032276665092538489>' in message.content and '!battle' not in message.content:
                roll = random.randint(1, 10)
                if roll > 4:
                    await message.channel.send('*slithers by*')
                elif roll == 3:
                    await message.channel.send('*blends into the surroundings*')
                elif roll == 2:
                    await message.channel.send('*munches on some bread*')
                elif roll == 1:
                    await message.reply('*bonks you* <:bonk:687841666182414413>')
        
        #@mod ping
            sqlCursor.execute('SELECT adminPingChannel, adminRoles FROM serverDB WHERE serverId = %s', (message.guild.id,))
            channelData = sqlCursor.fetchone()
            if channelData[0] != None and channelData[1] != None and message.author.id != 1032276665092538489:
                adminPingChannel = channelData[0]
                adminRoles = json.loads(channelData[1])
                #if '<@&423458739656458243>' in message.content:
                for x in adminRoles:
                    if str(x) in message.content:
                        embed=discord.Embed(title=f"Admin pinged by {message.author.display_name}", description=f"[\[Link\]]({message.jump_url})", color=0x00FF00)
                        embed.set_footer(text=timeNow())
                        await adminPingChannel.send(embed=embed)
                        await message.reply('Mods pinged!')

            await client.process_commands(message)
