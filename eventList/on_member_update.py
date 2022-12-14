import discord
from discord.ext import commands
import asyncio
from functions import *

def setup(client):
    @client.event #update user profiles to a channel whenever there's a change
    async def on_member_update(before, after):
        '''
        > activates upon member
            - leaving the server
            - changing nickname
            - changing roles
            - changing pfp
        
        > does not activate when member joins server
        '''
        sqlCursor.execute('SELECT userProfilesChannel FROM serverDB WHERE serverId = %s', (after.guild.id,))
        channelData = sqlCursor.fetchone()[0]
        if channelData != None:
            channel = client.get_channel(channelData) #user profiles channel
        
            await asyncio.sleep(5)

            if after.guild.get_member(after.id) is not None and checkRoles(after, [454948280825282560]) == False: #update if member still in server, and does not have the new member role
                found = 0
                async for message in channel.history(limit=None): # If member profile is found, update it 
                    if message.embeds and message.embeds[0].description and f'**User ID**: {after.id}' in message.embeds[0].description:
                        found = 1
                        notesStart = message.embeds[0].description.index('**Notes**:')
                        userName = after.name + "#" + after.discriminator
                        roleList = []
                        for x in after.roles:
                            roleList.append(x.name)

                        embed = discord.Embed(title=f'{after.display_name} ({userName})', description=f'**User ID**: {after.id}\n**User Roles**: {roleList}\n{message.embeds[0].description[notesStart:]}')
                        embed.set_thumbnail(url=after.display_avatar.url)
                        await message.edit(embed=embed)
                        break

                if found == 0: #Profile not found, creating new profile
                    userName = after.name + "#" + after.discriminator
                    roleList = []
                    for x in after.roles:
                        roleList.append(x.name)

                    embed = discord.Embed(title=f'{after.display_name} ({userName})', description=f'**User ID**: {after.id}\n**User Roles**: {roleList}\n**Notes**:\n**Infractions**:')
                    embed.set_thumbnail(url=after.display_avatar.url)
                    await channel.send(embed=embed)

                    await asyncio.sleep(5)
                    dupeCount = 0
                    async for message in channel.history(limit=10): # Deletes duplicate profiles if found
                        if message.embeds and message.embeds[0].description and f'**User ID**: {after.id}' in message.embeds[0].description:
                            dupeCount += 1
                            if dupeCount > 1:
                                await message.delete()
