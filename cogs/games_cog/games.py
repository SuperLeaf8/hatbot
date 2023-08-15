import discord
from discord.ext import commands
import random
import asyncio
import json
import os

class GamesCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # capital guesser ##########################################################################
    @commands.command()
    async def capitalguess(self, ctx):
        with open("capitals.json","r") as capitals_file: # json file containing dictionary of all countries and their capital(s)
            countries_capitals = json.load(capitals_file)
        country, capital = random.choice(list(countries_capitals.items()))
        # Send an embed message
        embed = discord.Embed(title="Guess the Capital", description=f"What is the capital of {country}?", color=discord.Color.magenta())
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
    ############################################################################################

    # flag guesser #############################################################################
    @commands.command()
    async def flagguess(self, ctx):
        with open("./cogs/games_cog/flags.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)


        rand_index = random.randint(0,len(data)-1)

        # Extract the country code
        country_code = data[rand_index]["code2l"]

        # URL template for flag images
        flag_url_template = "https://www.worldometers.info/img/flags/{0}-flag.gif"
        flag_url = flag_url_template.format(country_code.lower())

        print("Country Code:", country_code)
        print("Flag URL:", flag_url)

        # Send an embed message
        embed = discord.Embed(title="Guess the Country", description=f"What country does this flag belong to?", color=discord.Color.magenta())
        embed.set_image(url=flag_url)
        await ctx.send(embed=embed)

        # Function to check if the user's response is correct
        def check(m):
            return m.author == ctx.author and m.content.lower() == data[rand_index]['name'].lower()

        try:
            user_response = await self.bot.wait_for('message', check=check, timeout=60)
            await ctx.send(f"Correct! The flag belongs to {data[rand_index]['name']}.")
        except asyncio.TimeoutError:
            await ctx.send(f"60 second timer's up! The correct answer was {data[rand_index]['name']}.")
        
    @commands.command()
    async def unscramble(self, ctx):
        pass