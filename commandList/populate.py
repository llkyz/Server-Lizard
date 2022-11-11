import discord
from discord.ext import commands

def setup(client):
    @client.command() #populate the user profile channel
    async def populate(ctx): 
        if ctx.author.id == 262909760255426570:
            msg1 = await ctx.reply("Populating user profiles... sit tight!")
            channel = client.get_channel(1035131570257932318)
            for member in channel.guild.members:
                userName = member.name + "#" + member.discriminator
                roleList = []
                for x in member.roles:
                    roleList.append(x.name)

                embed = discord.Embed(title=f'{member.display_name} ({userName})', description=f'**User ID**: {member.id}\n**User Roles**: {roleList}\n**Infractions**:')
                embed.set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=embed)
                await asyncio.sleep(2)
            await msg1.reply("All done!")
