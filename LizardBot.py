import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import glob
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

myfolders = ["commandList/*.py", "commandList/messageCommandList/*.py", "commandList/userCommandList/*.py", "eventList/*.py", "admin/*.py"]

async def main():
    async with client:
        print("running main")
        for folderPath in myfolders:
            for x in glob.glob(folderPath):
                print(x)
                await client.load_extension(x.replace("\\", ".").replace("/", ".").replace(".py", ""))
        # await client.load_extension('commandList.test')
        await client.start(TOKEN)
        await client.tree.sync()


try:
    asyncio.run(main())
except discord.HTTPException as exception:
    print("HTTPException Occurred")
    if ("Retry-After" in exception.response.headers):
        print(f'Retry again after {exception.response.headers.get("Retry-After")} seconds')