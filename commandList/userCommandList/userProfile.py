import discord
from discord.ext import commands
from functions import *

def setup(client):
    @client.user_command(name="User Profile") #Looks up user's profile in the user profile channel
    async def userProfile(ctx, user):
        if hasAdminRole(ctx) or checkOwner(ctx):
            sqlCursor.execute('SELECT userProfilesChannel FROM serverDB WHERE serverId = %s', (ctx.guild.id,))
            channelData = sqlCursor.fetchone()[0]
            if channelData != None:
                channel = client.get_channel(channelData)
                found = 0
                
                async for message in channel.history(limit=None):
                    if message.embeds and message.embeds[0].description and f'**User ID**: {user.id}' in message.embeds[0].description:
                        await ctx.respond(f'User profile for {user.display_name} found at [\[link]]({message.jump_url})\nUser ID: {user.id}', ephemeral=True,delete_after=300)
                        found = 1
                        break
                if found == 0:
                    await ctx.respond(f'Profile can\'t be found?! Contact your local lizard support', ephemeral=True,delete_after=30)
        else:
            await ctx.respond(f'You are not authorized to use this command', ephemeral=True,delete_after=30)
