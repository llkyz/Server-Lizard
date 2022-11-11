import discord
from discord.ext import commands

def setup(client):
    @client.event
    async def on_raw_reaction_add(payload):
        if str(payload.emoji) == '⭐':
            channel = client.get_channel(payload.channel_id)
            myMessage = await channel.fetch_message(payload.message_id)
            reaction = discord.utils.get(myMessage.reactions, emoji='⭐')
            if (channel.id == 407561378564407297 or channel.id == 407561306162331674) and reaction.count >= 5:
                starChannel = client.get_channel(1032702775022321735)
                found = 0
                async for message in starChannel.history(limit=None):
                    if message.embeds and message.embeds[0].footer and f'Message ID: {myMessage.id}' in message.embeds[0].footer.text:
                        found = 1
                        await message.edit(content='** **' + '⭐' * reaction.count)
                        break
                if found == 0:
                    embed=discord.Embed(description=f'{reaction.message.content}\n\n> [\[Link\]]({reaction.message.jump_url})', color=0x14AB49)
                    embed.set_footer(text=f'brought to you by degens at #{reaction.message.channel} | Message ID: {myMessage.id}')
                    embed.set_author(name=f'{reaction.message.author.display_name}', icon_url=reaction.message.author.display_avatar)
                    if reaction.message.attachments:
                        embed.set_image(url=reaction.message.attachments[0].url)
                    await starChannel.send(content='** **' + '⭐' * reaction.count, embed=embed)
