import discord
from discord.ext import commands
from functions import *
import asyncio
from discord import Button, ButtonStyle

docs = {

    "aliases":[],

    "usage":"!embed create, !embed edit [msg id], !embed delete [msg id]",

    "description":"Placeholder. Requires embed role permission to use.",

    "category":"utility"
    
    }

def setup(client):
    @client.command()
    async def embed(ctx):
        if hasEmbedRole(ctx) or hasAdminRole(ctx) or checkOwner(ctx):
            msgData = ctx.message.content.split(" ")

            if len(msgData) == 1:
                await ctx.reply("Please use the following format: !embed create / !embed edit [msg id] / !embed delete [msg id]", delete_after=20)
            elif msgData[1].lower() == "create":
                await ctx.author.send(embed=discord.Embed(title=f'Creating new embed in `#{ctx.channel.name}` on {ctx.guild.name}'))

                mainTitle = "Title here"
                mainDescription = "Description here"
                mainColour = 0xaacbeb
                messageId = "<message ID here>"

                buttonColours = [ButtonStyle.blurple, ButtonStyle.grey, ButtonStyle.grey, ButtonStyle.grey, ButtonStyle.grey, ButtonStyle.green, ButtonStyle.red]

                #grey
                #green
                #red
                #blurple

                view = discord.ui.View()
                button1 = discord.ui.Button(label="Main Body", style=buttonColours[0], row=0, custom_id='main')
                button2 = discord.ui.Button(label="Fields", style=buttonColours[1], row=0, custom_id='fields')
                button3 = discord.ui.Button(label="Author", style=buttonColours[2], row=1, custom_id='author')
                button4 = discord.ui.Button(label="Image", style=buttonColours[3], row=1, custom_id='image')
                button5 = discord.ui.Button(label="Thumbnail", style=buttonColours[4], row=1, custom_id='thumbnail')
                button6 = discord.ui.Button(label="Create", style=buttonColours[5], row=2, custom_id='Create')
                button7 = discord.ui.Button(label="Cancel", style=buttonColours[6], row=2, custom_id='Cancel')
                view.add_item(item=button1)
                view.add_item(item=button2)
                view.add_item(item=button3)
                view.add_item(item=button4)
                view.add_item(item=button5)
                view.add_item(item=button6)
                view.add_item(item=button7)
                embed = discord.Embed(title=f'{mainTitle}', description=f'{mainDescription}', color=mainColour)
                embed.set_footer(text=f'created by {ctx.author.display_name} | Message ID: {messageId}')
                await ctx.author.send(embed=embed, view=view)

            elif msgData[1].lower() == "edit":
                pass
            elif msgData[1].lower() == "delete":
                pass
            else:
                await ctx.reply("Please use the following format: !embed create / !embed edit [msg id] / !embed delete [msg id]", delete_after=20)