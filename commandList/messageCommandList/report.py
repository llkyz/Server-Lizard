import discord
from discord.ext import commands
from functions import *
import asyncio


def setup(client):
    @client.message_command(name="Report Message")
    async def report(ctx: discord.ApplicationContext, message: discord.Message):
        sqlCursor.execute('SELECT reportChannel FROM serverDB WHERE serverId = %s', (message.guild.id,))
        channelData = sqlCursor.fetchone()[0]

        if channelData != None:
            reportChannel = client.get_channel(channelData) #reports channel

            view = discord.ui.View()
            options = []
            options.append(discord.SelectOption(label=f'Send a written report', value=f'modal'))
            options.append(discord.SelectOption(label=f'Report message for self-harm', value=f'selfHarm'))
            options.append(discord.SelectOption(label=f'Cancel', value=f'0'))
            myMenu = discord.ui.Select(placeholder="Select an option", options=options)
            view.add_item(myMenu)

            msg1 = await ctx.respond(view=view, ephemeral=True, delete_after=300)

            def checkButton(m):
                return m.application_id == msg1.application_id and m.user == ctx.author
            try:
                interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
            except asyncio.TimeoutError:
                await msg1.edit(content='Timed out!', view=None)
                return
            
            await msg1.delete_original_response()
            optionSelected = interacted.data["values"][0]
            
            if optionSelected == 'modal':
                report = ReportModal(title="Report Form")
                await interacted.response.send_modal(report)
                await report.wait()
                embed = discord.Embed(title=f'__Message Report__', description=f'**Sent by**: {ctx.user.display_name} (`{ctx.user}`)\n**Reported User**: {str(message.author.display_name)} (`{message.author}`)\n**Channel**: #{str(message.channel)}\n**Time**: ' + timeConvert(message.created_at) + f'\n**Message Link**: [\[Link\]]({message.jump_url})', color=0xFF5733)
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
                embed = discord.Embed(title=f'__Self-harm Report__', description=f'**Sent by**: {ctx.user.display_name} (`{ctx.user}`)\n**Reported User**: {str(message.author.display_name)} (`{message.author}`)\n**Channel**: #{str(message.channel)}\n**Time**: ' + timeConvert(message.created_at) + f'\n**Message Link**: [\[Link\]]({message.jump_url})', color=0xFF5733)
                embed.add_field(name="Message Content", value=f"> `{message.content}`", inline=False)
                embed.set_footer(text=timeNow())
                if message.attachments:
                    embed.set_image(url=message.attachments[0].url)
                await reportChannel.send(embed=embed)
                await interacted.response.send_message("Thank you, your report has been sent.", ephemeral=True, delete_after=20)

        else:
            await ctx.respond("This feature has not been activated.", ephemeral=True, delete_after=20)
    
    class ReportModal(discord.ui.Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.add_item(discord.ui.InputText(label="Details on why this post was reported", style=discord.InputTextStyle.long))
            self.add_item(discord.ui.InputText(label="Additional supporting links/messages", style=discord.InputTextStyle.long, required=False))

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message('Thank you, your report has been sent.', ephemeral=True, delete_after=30)

