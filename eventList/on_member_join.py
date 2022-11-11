import discord
from discord.ext import commands

def setup(client):
    @client.event #if a user profile already exists, posts user's previous roles to the notice channel
    async def on_member_join(member):
        profileChannel = client.get_channel(1035131570257932318)
        newcomerChannel = client.get_channel(535480699981922324)
        async for message in profileChannel.history(limit=None):
            if message.embeds:
                if message.embeds[0].description and f'**User ID**: {member.id}' in message.embeds[0].description:
                    mystr = message.embeds[0].description.replace("\n**Infractions**:","")
                    mystr = mystr.split("**User Roles**: ")
                    embed = discord.Embed(title=f'{member.display_name} rejoined the server', description=f'Their roles were: {mystr[1]}')
                    await newcomerChannel.send(embed=embed)
                    break
