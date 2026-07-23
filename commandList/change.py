import discord
from discord.ext import commands
import random

docs = {

    "aliases":[],

    "usage":"!change",

    "description":"Changes my nickname! Beware, may have certain unforseen side effects. Use at your own risk... 🦎",

    "category":"fluff"
    
    }

async def setup(client):
    @client.command() #!change
    async def change(ctx):
        roll = random.randint(1, 20)
        if roll > 4:
            myname = "Server Li" + ("z" * random.randint(0,13)) + "ard"
            await ctx.send(f"Changed name to {myname}!")
        elif roll == 4:
            myname = "L̶̨͐͋i̵̙̳̹̾͒͝z̷͓̰̗̃̇a̸͕̒ŕ̸͍̙̣͘d̤̙͖"
            await ctx.send(f"₵Ⱨ₳₦₲ɆĐ ₦₳₥Ɇ ₮Ø ₴ɆⱤVɆⱤ {myname}")
        elif roll == 3:
            myname = "🤖🦎"
            await ctx.send(f"** **📝🔄➡🤖🦎")
        elif roll <= 2:
            myname = ""
            await ctx.send(f"Stop changing my name! 😠")
        await ctx.guild.me.edit(nick=myname)
