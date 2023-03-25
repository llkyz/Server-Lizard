import discord
from discord import Button, ButtonStyle
from discord.ext import commands
from functions import *
import asyncio

docs = {

    "aliases":[],

    "usage":"!lizard [optional: buy/sell]",

    "description":"Get a golden lizard for the low low price of 1,000,000,000 coins! Owning a golden lizard will make your coins animated! Also sellable at any time for 900,000,000 coins.",

    "category":"economy"
    
    }

def setup(client):
    @client.command() # Give another user some coins
    async def lizard(ctx, arg=None):
        goldenLizard = "<:golden_lizard:1055859182319968376>"
        userData = await fetchUserData(ctx.author)
        if arg == "buy":
            if userData["coins"] >= 1000000000:
                if userData["goldenLizard"] == None or userData["goldenLizard"] == 0:
                    lizardCount = 1
                else:
                    lizardCount = userData["goldenLizard"] + 1
                sql = 'UPDATE userDB SET goldenLizard = %s, coins = (coins - 1000000000) WHERE userId = %s'
                val = (lizardCount, ctx.author.id)
                sqlCursor.execute(sql, val)
                await ctx.send(f"{goldenLizard} | You bought a golden lizard for **1,000,000,000** coins!")
                return
            else:
                await ctx.send("You don't have enough coins to buy a golden lizard!")
                return
        elif arg == "sell":
            if userData["goldenLizard"] == None or userData["goldenLizard"] == 0:
                await ctx.send("You don't have any golden lizards to sell!")
                return
            elif userData["coins"] > 1247483647:
                view = discord.ui.View()
                button1 = discord.ui.Button(label="Confirm", style=ButtonStyle.green, custom_id='confirm')
                button2 = discord.ui.Button(label="Cancel", style=ButtonStyle.red, custom_id='cancel')
                view.add_item(item=button1)
                view.add_item(item=button2)
                mymsg = await ctx.send("Selling a golden lizard will cause you to exceed your coin limit! Do you wish to proceed?", view=view)

                def checkButton(m):
                    return m.message == mymsg and m.user == ctx.author

                try:
                    interacted = await client.wait_for('interaction', timeout=300, check=checkButton)
                except asyncio.TimeoutError:
                    view.clear_items()
                    await mymsg.edit(content='Timed out!', view=view)
                else:
                    await interacted.response.defer()
                    await mymsg.delete()

                    if interacted.data['custom_id'] == 'cancel':
                        await ctx.send("Sell cancelled", delete_after=20)
                        return
                    elif interacted.data['custom_id'] == 'confirm':
                        pass

            sql = 'UPDATE userDB SET goldenLizard = (goldenLizard - 1), coins = LEAST(coins + 900000000, 2147483647) WHERE userId = %s'
            val = (ctx.author.id,)
            sqlCursor.execute(sql, val)
            await ctx.send(f"{goldenLizard} | {ctx.author.display_name} You sold a golden lizard for **900,000,000** coins!")
            return

        else:
            if userData["goldenLizard"] == None or userData["goldenLizard"] == 0:
                await ctx.send(f"**{goldenLizard} | {ctx.author.display_name}** You have **0** golden lizards!")
            elif userData["goldenLizard"] == 1:
                await ctx.send(f'**{goldenLizard} | {ctx.author.display_name}** You have **1** golden lizard!')
            else:
                await ctx.send(f'**{goldenLizard} | {ctx.author.display_name}** You have **{userData["goldenLizard"]}** golden lizards!')