import discord
from discord.ext import commands
from discord import app_commands
from functions import *
from functions.sql_start import SQLObject
import asyncio

async def setup(client):
    @app_commands.context_menu(name="Report Message")
    async def report(interaction: discord.Interaction, message: discord.Message):
        SQLObject.execute('SELECT reportChannel FROM serverDB WHERE serverId = %s', (message.guild.id,))
        channelData = SQLObject.fetchone()[0]

        if channelData != None:
            reportChannel = client.get_channel(channelData) #reports channel

            view = discord.ui.View()
            options = [
                (discord.SelectOption(label=f'Send a written report', value=f'modal')),
                (discord.SelectOption(label=f'Report message for self-harm', value=f'selfHarm')),
                (discord.SelectOption(label=f'Cancel', value=f'0'))
            ]
            myMenu = discord.ui.Select(placeholder="Select an option", options=options)
            view.add_item(myMenu)

            await interaction.response.send_message(view=view, ephemeral=True, delete_after=300)

            msg1 = await interaction.original_response()

            def checkButton(m):
                return m.message.id == msg1.id and m.user.id == interaction.user.id
            
            try:
                interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
            except asyncio.TimeoutError:
                await msg1.edit(content='Timed out!', view=None)
                return
            
            await msg1.delete()
            optionSelected = interacted.data["values"][0]

            if optionSelected == 'modal':
                print(1)
                report = ReportModal()
                print(2)
                await interacted.response.send_modal(report)
                print(3)
                await report.wait()
                print(4)
                embed = discord.Embed(title=f'__Message Report__', description=f'**Sent by**: {interaction.user.display_name} (`{interaction.user}`)\n**Reported User**: {str(message.author.display_name)} (`{message.author}`)\n**Channel**: #{str(message.channel)}\n**Time**: ' + timeConvert(message.created_at) + f'\n**Message Link**: [\[Link\]]({message.jump_url})', color=0xFF5733)
                embed.add_field(name="Message Content", value=f"> `{message.content}`", inline=False)
                embed.add_field(name="Report Details", value=report.children[0].value, inline=False)
                embed.set_footer(text=timeNow())
                if message.attachments:
                    embed.set_image(url=message.attachments[0].url)
                if report.children[1].value != "":
                    additionalInfo = report.children[1].value
                else:
                    additionalInfo = 'N/A'
                embed.add_field(name="Additional Info", value=additionalInfo, inline=False)
                await reportChannel.send(embed=embed)

            elif optionSelected == 'selfHarm':
                embed = discord.Embed(title=f'__Self-harm Report__', description=f'**Sent by**: {interaction.user.display_name} (`{interaction.user}`)\n**Reported User**: {str(message.author.display_name)} (`{message.author}`)\n**Channel**: #{str(message.channel)}\n**Time**: ' + timeConvert(message.created_at) + f'\n**Message Link**: [\[Link\]]({message.jump_url})', color=0xFF5733)
                embed.add_field(name="Message Content", value=f"> `{message.content}`", inline=False)
                embed.set_footer(text=timeNow())
                if message.attachments:
                    embed.set_image(url=message.attachments[0].url)
                await reportChannel.send(embed=embed)
                await interacted.response.send_message("Thank you, your report has been sent.", ephemeral=True, delete_after=20)

        else:
            await interaction.response.send_message("This feature has not been activated.", ephemeral=True, delete_after=20)
    
    class ReportModal(discord.ui.Modal, title="Report Form"):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.add_item(discord.ui.TextInput(label="Details on why this post was reported", style=discord.TextStyle.paragraph))
            self.add_item(discord.ui.TextInput(label="Additional supporting links/messages", style=discord.TextStyle.paragraph, required=False))

        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.send_message('Thank you, your report has been sent.', ephemeral=True, delete_after=30)

    client.tree.add_command(report)