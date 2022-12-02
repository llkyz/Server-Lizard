import discord
from discord.ext import commands
import importlib
import glob

docs = {

    "aliases":['command', 'help'],

    "usage":"!commands",

    "description":"Displays a list of my commands. Type `!` followed by the command's name to use it.",

    "category":"utility"
    
    }

def setup(client):
    client.remove_command('help')
    @client.command(aliases=['command','help']) #!commands            
    async def commands(ctx, arg=None):
        categories = {
            "utility": {'field': "🔧 **Utility**", 'modules':[]},
            "fluff": {'field': "🙃 **Fluff**", 'modules':[]},
            "economy": {'field': "🪙 **Economy**", 'modules':[]},
            "games": {'field': "🎮 **Games**", 'modules':[]},
            "gamble": {'field': "🎲 **Gamble**", 'modules':[]},
            "messages": {'field': "📰 **Message Management**", 'modules':[]},
            "admin": {'field': "👓 **Mod/Admin Use**", 'modules':[]},
        }

        if arg == None:
            commandList = glob.glob("commandList/*.py")
            for x in commandList:
                slice = x.replace("\\", ".").replace("/", ".").replace(".py", "")
                commandName = slice.replace("commandList.","")
                getDocs = importlib.import_module(slice)
                if getDocs.docs["category"] in categories:
                    categories[getDocs.docs["category"]]["modules"].append(f'`{commandName}`')

            embed=discord.Embed(title=f'Lizard Commands!', description='Use !help or !commands to show this list.\nTo use a command, type: `![command]`.\nTo get additional info on a command, type: `!command [commmand name]`',color=0x14AB49)
            for key in categories:
                embed.add_field(name=categories[key]["field"], value=" ".join(categories[key]["modules"]), inline=False)
            embed.add_field(name='**Additional Features**', value='Starboard / Post Reporting / Mod Pings', inline=False)
            await ctx.reply(embed=embed)

        else:
            try:
                mymodule = "commandList."
                getDocs = importlib.import_module(mymodule + arg)
                if getDocs.docs["category"] not in categories:
                    await ctx.reply("Command not found!")
                else:
                    if len(getDocs.docs["aliases"]) == 0:
                        aliasList = "None"
                    else:
                        aliasList = ", ".join(getDocs.docs["aliases"])

                    embed = discord.Embed(title=f'[Command] !{arg}', description=f'**Aliases**: {aliasList}\n\n**Usage**: {getDocs.docs["usage"]}\n\n**Description**\n> {getDocs.docs["description"]}', color=0xaacbeb)
                    await ctx.reply(embed=embed)
            except:
                await ctx.reply("Command not found!")