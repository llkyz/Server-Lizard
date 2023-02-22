import discord
from discord.ext import commands
from discord import Button, ButtonStyle
import random
import asyncio
from functions import *

docs = {

    "aliases":['overwrite'],

    "usage":"!overwrites [channel id]",

    "description":"Retrieves permission overwrites for all roles for the specified channel",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command(aliases=['permission'])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def overwrites(ctx, arg=None):
        if not hasAdminRole(ctx) and not checkOwner(ctx):
            return
        
        if arg == None:
            ctx.reply("Please specify a channel ID")
            return
        
        allRoles = ctx.guild.roles
        channel = client.get_channel(int(arg))
        overwrites = channel.overwrites
        permList = ['add_reactions','administrator',
            'attach_files',
            'ban_members',
            'change_nickname',
            'connect',
            'create_instant_invite',
            'create_private_threads',
            'create_public_threads',
            'deafen_members',
            'embed_links',
            'external_emojis',
            'external_stickers',
            'kick_members',
            'manage_channels',
            'manage_emojis',
            'manage_emojis_and_stickers',
            'manage_events',
            'manage_guild',
            'manage_messages',
            'manage_nicknames',
            'manage_permissions',
            'manage_roles',
            'manage_threads',
            'manage_webhooks',
            'mention_everyone',
            'moderate_members',
            'move_members',
            'mute_members',
            'priority_speaker',
            'read_message_history',
            'read_messages',
            'request_to_speak',
            'send_messages',
            'send_messages_in_threads',
            'send_tts_messages',
            'speak',
            'stream',
            'use_application_commands',
            'use_external_emojis',
            'use_external_stickers',
            'use_voice_activation',
            'view_audit_log',
            'view_channel',
            'view_guild_insights']
        data = []
        output = f'**Overwrites for #{channel}**\n===================\n'
        for x in overwrites:
            data.append({x: []})
            output += f'{x}\n-----\n'
            for y in permList:
                myPerm = getattr(overwrites[x], y)
                if myPerm != None:
                    output += f'{y}: {myPerm}\n'

            output += f'-----\n\n'

        await ctx.reply(output)