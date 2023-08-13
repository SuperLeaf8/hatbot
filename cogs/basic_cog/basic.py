import discord
from discord.ext import commands
import random
import asyncio
import json

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # gives the cog a bot instance so we can do bot stuff LOL! ex:    self.bot.name returns bot name
    
    @commands.command()
    async def test(self, ctx, bollocks):
        await ctx.respond('test')
        await ctx.send(bollocks)

    @commands.command()
    async def guess(self, ctx):
        with open("capitals.json","r") as capitals_file: # move json to somwhere more organized and not just thrown in here, or maybe keep it here because relevant?
            countries_capitals = json.load(capitals_file)
        country, capital = random.choice(list(countries_capitals.items()))

        # Send an embed message
        embed = discord.Embed(title="Guess the Capital", description=f"What is the capital of {country}?", color=discord.Color.blue())
        await ctx.send(embed=embed)

        # Function to check if the user's response is correct
        def check(m):
            return m.author == ctx.author and m.content.lower() == capital.lower()

        try:
            user_response = await self.bot.wait_for('message', check=check, timeout=20)
        except asyncio.TimeoutError:
            await ctx.send(f"Time's up! The correct answer was {capital}.")
        else:
            await ctx.send(f"Correct! {capital} is the capital of {country}.")
