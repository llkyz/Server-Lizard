import discord
from discord.ext import commands
import asyncio

docs = {

    "aliases":[],

    "usage":"!populate",

    "description":"Populate the selected channel with user profiles. This may take anywhere from a few minutes to a few hours depending on the size of your server. The message \"All done!\" will be sent upon completion.",

    "category":"admin-administrative"
    
    }

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
