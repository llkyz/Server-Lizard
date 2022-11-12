import discord
from discord.ext import commands

def checkOwner(ctx):
    if ctx.author.id == 262909760255426570:
        return True