import discord
from discord.ext import commands
from functions import *

def setup(client):
    @client.event #if a user profile already exists, posts user's previous roles to the notice channel
    async def on_member_join(member):
        sqlCursor.execute('SELECT userProfilesChannel, saveRoleChannel FROM serverDB WHERE serverId = %s', (member.guild.id,))
        channelData = sqlCursor.fetchone()

        if channelData[0] != None and channelData[1] != None:
            profileChannel = client.get_channel(channelData[0])
            newcomerChannel = client.get_channel(channelData[1])
            async for message in profileChannel.history(limit=None):
                if message.embeds:
                    if message.embeds[0].description and f'**User ID**: {member.id}' in message.embeds[0].description:
                        mystr = message.embeds[0].description.replace("\n**Infractions**:","")
                        mystr = mystr.split("**User Roles**: ")
                        embed = discord.Embed(title=f'{member.display_name} rejoined the server', description=f'{member.mention}\'s roles were: {mystr[1]}')
                        await newcomerChannel.send(embed=embed)
                        break