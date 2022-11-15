import discord
from discord.ext import commands

#usage example: checkRoles(ctx.author, [1030144135560167464, 1035245311553196112])
#returns True if any of the roles in the array matches, else return False
def checkRoles(member, arr):
    for x in member.roles:
        if x.id in arr:
            return True
    return False