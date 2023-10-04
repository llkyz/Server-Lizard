import discord
from discord.ext import commands
from discord import File
from functions import *
import io
import json
import asyncio
from discord import Button, ButtonStyle

docs = {

    "aliases":[],

    "usage":"!getroleusers [@role]",

    "description":"Get a list of users and their user ID with a specified role.",

    "category":"admin-administrative"
    
    }

def setup(client):
    @client.command()
    async def getroleusers(ctx, role: discord.Role):
        if not hasAdminRole(ctx) and checkOwner(ctx):
            await ctx.reply("You do not have permission to use this command!", delete_after=20)
            return

        if role == None:
            await ctx.reply('Please enter a role. Please use `!getroleusers [@role]`', delete_after=20)
            return
        myList = "\n".join(str(f'{member}, {member.id}') for member in role.members)
        f = io.StringIO(myList)
        await ctx.send(content=f"List of members with {role} role", file=File(fp=f, filename="user_info.txt"))