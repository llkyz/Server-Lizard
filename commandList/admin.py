import discord
from discord.ext import commands
import importlib
import glob
from functions import *

docs = {

    "aliases":[],

    "usage":"!admin",

    "description":"Displays a list of admin-exclusive commands. Requires administrator permission to use.",

    "category":"admin"
    
    }

categories = {
    "admin-messages": {'field': "📰 **Message Management**", 'modules':[]},
    "admin-administrative": {'field': "👓 **Administrative**", 'modules':[]},
    "admin-disciplinary": {'field': "❌ **Disciplinary**", 'modules':[]},
}

def setup(client):
    @client.command() #!admin
    async def admin(ctx):
        if hasAdminRole(ctx) or checkOwner(ctx):
            msgData = ctx.message.content.split(" ")
            if len(msgData) == 1:
                commandList = glob.glob("commandList/*.py")
                for x in commandList:
                    slice = x.replace("\\", ".").replace("/", ".").replace(".py", "")
                    commandName = slice.replace("commandList.","")
                    getDocs = importlib.import_module(slice)
                    if getDocs.docs["category"] in categories:
                        categories[getDocs.docs["category"]]["modules"].append(f'`{commandName}`')

                embed=discord.Embed(title=f'Admin commands for Server Lizard', description='To use a command, type: `![command]`.\nTo get additional info on a command, type: `!admin [commmand name]`',color=0x14AB49)
                for key in categories:
                    embed.add_field(name=categories[key]["field"], value=" ".join(categories[key]["modules"]), inline=False)
                await ctx.reply(embed=embed)

            else:
                try:
                    mymodule = "commandList."
                    getDocs = importlib.import_module(mymodule + msgData[1])
                    if getDocs.docs["category"] not in categories:
                        await ctx.reply("Command not found!")
                    else:
                        if len(getDocs.docs["aliases"]) == 0:
                            aliasList = "None"
                        else:
                            aliasList = ", ".join(getDocs.docs["aliases"])

                        embed = discord.Embed(title=f'[Command] !{msgData[1]}', description=f'**Aliases**: {aliasList}\n\n**Usage**: {getDocs.docs["usage"]}\n\n**Description**\n> {getDocs.docs["description"]}', color=0xaacbeb)
                        await ctx.reply(embed=embed)
                except:
                    await ctx.reply("Command not found!")