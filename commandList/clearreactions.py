import discord
from functions import *

docs = {

    "aliases":['clearReaction', 'removeReactions', 'removeReaction'],

    "usage":"!clearReactions",

    "description":"Reply to a message with this command to clear all reactions from that message.",

    "category":"admin-messages"
    
    }

def setup(client):
    @client.command(aliases=['clearreactions', 'clearReaction', 'clearreaction', 'removeReactions', 'removereactions', 'removeReaction', 'removereaction'])
    async def clearReactions(ctx):
        if hasAdminRole(ctx) or checkOwner(ctx):
            if ctx.message.reference is not None:
                channel = await client.fetch_channel(ctx.message.reference.channel_id)
                message = await channel.fetch_message(ctx.message.reference.message_id)
                await message.clear_reactions()
                await ctx.reply(embed=discord.Embed(title="Reactions cleared"))
            else:
                await ctx.reply("Please reply to a message with this command.", delete_after=20)