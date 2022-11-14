import discord
from discord.ext import commands
import datetime
import requests
import json
import math
from dotenv import load_dotenv
import os

def setup(client):
    @client.command() #!bus
    async def bus(ctx):
        msgData = ctx.message.content.split(" ")
        if len(msgData) == 2:
            if msgData[1].isnumeric() and len(msgData[1]) == 5:
                load_dotenv()
                ACCOUNTKEY = os.getenv('LTA_KEY')
                BASE_API_DOMAIN = 'http://datamall2.mytransport.sg/ltaodataservice'
                BUS_ARRIVAL_API_ENDPOINT = '{}/BusArrivalv2'.format(BASE_API_DOMAIN)

                response = requests.get(BUS_ARRIVAL_API_ENDPOINT, params={'BusStopCode':msgData[1]}, headers={'method': 'GET', 'AccountKey': ACCOUNTKEY, 'accept': 'application/json'})
                mydict = json.loads(response.content.decode('utf-8'))

                currentTime = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
                nextBusArr = ["NextBus","NextBus2","NextBus3"]

                def processTime(timestamp):
                    return datetime.datetime.fromisoformat(timestamp)

                def calcArrival(arriving, timenow):
                    start = datetime.datetime.combine(arriving.date(), arriving.time(), None)
                    end = datetime.datetime.combine(timenow.date(), timenow.time(), None)
                    result = start - end
                    result = math.floor(result.seconds / 60)
                    if result > 100 or result == 0:
                        return ("`Arr`")
                    else:
                        return (f'`{result}m`')

                if len(mydict["Services"]) == 0:
                    await ctx.reply("Invalid bus stop code!", delete_after=20)
                else:
                    embedData = []

                    for x in mydict["Services"]:
                        tempHolder = []
                        for y in range(3):
                            if nextBusArr[y] in x:
                                busArrival = processTime(x[nextBusArr[y]]["EstimatedArrival"])
                                tempHolder.append(calcArrival(busArrival, currentTime))
                            else:
                                tempHolder.append("N/A")

                        embedData.append({'service': f'__**{x["ServiceNo"]}**__', 'timings': tempHolder})   

                    embed = discord.Embed(title=f'Bus Stop {msgData[1]}')
                    for x in embedData:
                        embed.add_field(name=x["service"], value="\n".join(x["timings"]), inline=True)
                    await ctx.reply(embed=embed)
            else:
                await ctx.reply("Please use the following format: !bus [5 digit bus stop code]", delete_after=20)
        else:
            await ctx.reply("Please use the following format: !bus [5 digit bus stop code]", delete_after=20)