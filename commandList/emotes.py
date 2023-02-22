import discord
from discord.ext import commands
from functions import *
import requests
import json

docs = {

    "aliases":[''],

    "usage":"N/A",

    "description":"Placeholder",

    "category":"fluff"
    
    }

async def emoteAction(client, ctx, arg, emoteCommand):
    try:
        userId = int(arg.replace('<@','').replace('>',''))
        guild = await client.fetch_guild(ctx.guild.id)
        getUser = await guild.fetch_member(userId)
    except:
        await ctx.reply(f'Oops, please use !{emoteCommand} [@user]!')
        return
    emoteResponse = {
        'hug': f'**{ctx.author.display_name}** gives **{getUser.display_name}** a big hug! 🤗',
        'cuddle': f'**{ctx.author.display_name}** cuddles up to **{getUser.display_name}**! Aww...',
        'kiss': f'**{ctx.author.display_name}** gives **{getUser.display_name}** a kiss! Muacks! 💋',
        'pat': f'**{ctx.author.display_name}** pats **{getUser.display_name}** on the head...',
        'poke': f'**{ctx.author.display_name}** pokes **{getUser.display_name}**! Ow!',
        'wave': f'**{ctx.author.display_name}** waves at **{getUser.display_name}**! Hi there~'
        }
    emoteSelf = {
        'hug': f'**{ctx.author.display_name}** gives themself a big hug! Here\'s some extra love! 🤗🤗🤗',
        'cuddle': f'**{ctx.author.display_name}** cuddles up to themself~ 🥹',
        'kiss': f'**{ctx.author.display_name}** spontaneously generates a second mouth and gives themself a kiss! Muacks! 💋',
        'pat': f'**{ctx.author.display_name}** pats themself on the head. Aw.',
        'poke': f'**{ctx.author.display_name}** pokes themself. It\'s not very effective...',
        'wave': f'**{ctx.author.display_name}** waves at themself...? How??'
        }
    response = requests.get(f'https://api.otakugifs.xyz/gif?reaction={emoteCommand}')
    myImage = json.loads(response.content.decode('utf-8'))['url']
    if ctx.author == getUser:
        embed=discord.Embed(description=emoteSelf[emoteCommand], color=0x87ceeb)
    else:
        embed=discord.Embed(description=emoteResponse[emoteCommand], color=0x87ceeb)
    embed.set_image(url=myImage)
    await ctx.send(embed=embed)


def setup(client):
    @client.command()
    async def hug(ctx, arg):
        await emoteAction(client, ctx, arg, 'hug')

    @client.command()
    async def cuddle(ctx, arg):
        await emoteAction(client, ctx, arg, 'cuddle')

    @client.command()
    async def kiss(ctx, arg):
        await emoteAction(client, ctx, arg, 'kiss')

    @client.command()
    async def pat(ctx, arg):
        await emoteAction(client, ctx, arg, 'pat')

    @client.command()
    async def poke(ctx, arg):
        await emoteAction(client, ctx, arg, 'poke')

    @client.command()
    async def wave(ctx, arg):
        await emoteAction(client, ctx, arg, 'wave')

