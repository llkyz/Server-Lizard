import discord
from discord.ext import commands
from discord import app_commands
from discord import Button, ButtonStyle
from functions import *
from functions.sql_start import SQLObject

async def setup(client):
    @app_commands.context_menu(name="User Profile") #Looks up user's profile in the user profile channel
    async def userProfile(interaction: discord.Interaction, user: discord.User):
        if hasAdminRole(interaction) or checkOwner(interaction):
            SQLObject.execute('SELECT userProfilesChannel FROM serverDB WHERE serverId = %s', (interaction.guild.id,))
            channelData = SQLObject.fetchone()[0]
            if channelData != None:
                channel = client.get_channel(channelData)
                found = 0
                
                async for message in channel.history(limit=None):
                    if message.embeds and message.embeds[0].description and f'**User ID**: {user.id}' in message.embeds[0].description:
                        view = discord.ui.View()
                        button1 = discord.ui.Button(label="Source", style=ButtonStyle.gray, url=message.jump_url)
                        view.add_item(item=button1)
                        embed = discord.Embed(title=message.embeds[0].title, description=message.embeds[0].description)
                        embed.set_thumbnail(url=user.display_avatar.url)
                        await interaction.response.send_message(embed=embed, view=view, ephemeral=True, delete_after=300)
                        found = 1
                        break
                if found == 0:
                    await interaction.response.send_message(f'Profile can\'t be found?! Contact your local lizard support', ephemeral=True,delete_after=30)
            else:
                await interaction.response.send_message(f'A User Profile channel has not been set yet. Please set one up using `!userprofiles` and generate the profiles first.', ephemeral=True,delete_after=30)
        else:
            await interaction.response.send_message(f'You are not authorized to use this command', ephemeral=True,delete_after=30)
