import discord
from discord.ext import commands
import requests
import json
import random
from functions import *

docs = {

    "aliases":[],

    "usage":"!blahaj",

    "description":"Checks IKEA's stock to see if BLÅHAJ 🦈 and SMÖLHAJ 🦈 are available for sale. (Singapore-exclusive feature!)",

    "category":"fluff"
    
    }

def setup(client):
    @client.command() #!blahaj
    async def blahaj(ctx):
        storeList = ['Tampines', 'Alexandra', 'Jurong', 'Online']

        url = 'https://api.ingka.ikea.com/cia/availabilities/ru/sg?itemNos=10373589&expand=StoresList,Restocks,SalesLocations'
        headers = {'accept': 'application/json;version=2',
        'x-client-id': 'b6c117e5-ae61-4ef5-b4cc-e0b1e37f0631',
        }

        response = requests.get(url, headers=headers)
        mydict = json.loads(response.content.decode('utf-8'))

        blahajStock = {}
        for x in range(3):
            blahajStock[storeList[x]] = mydict['availabilities'][x]['buyingOption']['cashCarry']['availability']['probability']['thisDay']['messageType'].replace('_',' ')
        blahajStock[storeList[3]] = mydict['availabilities'][3]['buyingOption']['homeDelivery']['availability']['probability']['thisDay']['messageType'].replace('_',' ')

        url2 = 'https://api.ingka.ikea.com/cia/availabilities/ru/sg?itemNos=00540664&expand=StoresList,Restocks,SalesLocations'

        response = requests.get(url2, headers=headers)
        mydict = json.loads(response.content.decode('utf-8'))

        smohajStock = {}
        for x in range(3):
            smohajStock[storeList[x]] = mydict['availabilities'][x]['buyingOption']['cashCarry']['availability']['probability']['thisDay']['messageType'].replace('_',' ')
        smohajStock[storeList[3]] = mydict['availabilities'][3]['buyingOption']['homeDelivery']['availability']['probability']['thisDay']['messageType'].replace('_',' ')
        
        blahajNo = ["https://i.redd.it/vg3vjkroytq71.jpg",
                      "https://i.redd.it/2f72lz7qufm81.jpg",
                      "https://i.redd.it/fxckzsfrivq71.png",
                      "https://i.redd.it/zqb38mi2lcp91.jpg",
                      "https://i.redd.it/0963hzs2lcp91.jpg",
                      "https://static.mothership.sg/1/2022/01/272744499_10165925896085402_5819381897009474509_n.jpeg",]

        blahajYes = ["https://www.ikea.com/sg/en/images/products/blahaj-soft-toy-shark__0710175_pe727378_s5.jpg",
                     "https://media.tenor.com/JpairZOomiEAAAAd/bl%C3%A5haj-ikea-shark.gif",
                     "https://media.tenor.com/GAR9pKKpnIEAAAAC/shonk-shonks.gif",
                     "https://media.tenor.com/e7p3zXTC2owAAAAd/blahaj-ikea.gif",
                     "https://media.tenor.com/eNDOA4cQmNYAAAAd/blahaj-cat.gif",
                     "https://media.tenor.com/3a_BHoflOosAAAAd/blahaj-shark.gif",
                     "https://truth.bahamut.com.tw/s01/202204/f514f0295b7ac37df5d7911ffb143fb6.JPG"]
        
        if (blahajStock['Tampines'] == blahajStock['Alexandra'] == blahajStock['Jurong'] == blahajStock['Online'] == smohajStock['Tampines'] == smohajStock['Alexandra'] == smohajStock['Jurong'] == smohajStock['Online'] == "OUT OF STOCK"):
            embedColour = 0xFF5733
            embedImage = blahajNo[random.randint(0,len(blahajNo)-1)]
        else:
            embedColour = 0x00FF00
            embedImage = blahajYes[random.randint(0,len(blahajYes)-1)]
            
        embed=discord.Embed(title="BLÅHAJ Availability", description="Get your BLÅHAJ before they're gone!\n[BLÅHAJ (100cm)](https://www.ikea.com/sg/en/p/blahaj-soft-toy-shark-10373589/)\n[SMÖLHAJ (55cm)](https://www.ikea.com/sg/en/p/blahaj-soft-toy-baby-shark-00540664/)", color=embedColour)
        embed.set_image(url=embedImage)
        embed.add_field(name="BLÅHAJ", value="> Online: " + blahajStock["Online"] + "\n> Alexandra: " + blahajStock["Alexandra"] + "\n> Jurong: " + blahajStock["Jurong"] + "\n> Tampines: " + blahajStock["Tampines"], inline=True)
        embed.add_field(name="SMÖLHAJ", value="> Online: " + smohajStock["Online"] + "\n> Alexandra: " + smohajStock["Alexandra"] + "\n> Jurong: " + smohajStock["Jurong"] + "\n> Tampines: " + smohajStock["Tampines"], inline=True)
        embed.set_footer(text=timeNow())
        await ctx.send(embed=embed)
