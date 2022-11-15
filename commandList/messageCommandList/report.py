import discord
from discord.ext import commands
from functions import *


def setup(client):
    @client.message_command(name="Report Message")
    async def report(ctx: discord.ApplicationContext, message: discord.Message):
        report = ReportModal(title="Report Form")
        await ctx.send_modal(report)
        await report.wait()
        embed = discord.Embed(title=f'__**Post report by {ctx.user.display_name} ({ctx.user})**__', description=f'**Reported User**: {str(message.author.display_name)} ({message.author})\n**Channel**: #{str(message.channel)}\n**Time**: ' + timeConvert(message.created_at) + f'\n**Message Link**: [\[Link\]]({message.jump_url})', color=0xFF5733)
        embed.add_field(name="Message Content", value=f"> `{message.content}`", inline=False)
        embed.add_field(name="Reporting Details", value=report.children[0].value, inline=False)
        embed.set_footer(text=timeNow())
        if message.attachments:
            embed.set_image(url=message.attachments[0].url)
        if report.children[1].value != "":
            additionalInfo = report.children[1].value
        else:
            additionalInfo = 'N/A'
        embed.add_field(name="Additional Info", value=additionalInfo, inline=False)
        reportChannel = client.get_channel(1033289784581427230)
        await reportChannel.send(embed=embed)
    
    class ReportModal(discord.ui.Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.add_item(discord.ui.InputText(label="Details on why this post was reported", style=discord.InputTextStyle.long))
            self.add_item(discord.ui.InputText(label="Additional supporting links/messages", style=discord.InputTextStyle.long, required=False))

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.send_message('Report received.', ephemeral=True, delete_after=30)

