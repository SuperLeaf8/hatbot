import discord
from discord.ext import commands
import requests
import random

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # gives the cog a bot instance so we can do bot stuff LOL! ex:    self.bot.name returns bot name
    
    @commands.command()
    async def test(self, ctx, bollocks):
        await ctx.respond('test')
        await ctx.send(bollocks)
    
    @commands.command()
    async def get_avatar(self, ctx, user: discord.User):
        avatar_url = user.avatar_url

        embed = discord.Embed(title=f"Avatar of {user.display_name}", color=user.color)
        embed.set_image(url=avatar_url)

        await ctx.send(embed=embed)
    
    @commands.command()
    async def cat(self, ctx):
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        data = response.json()

        if data:
            cat_image_url = data[0]["url"]

            embed = discord.Embed(title="Random Cat Image", color=discord.Color.random())
            embed.set_image(url=cat_image_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch cat image.")
    
    @commands.command()
    async def dog(self, ctx):
        response = requests.get("https://random.dog/woof.json")
        data = response.json()

        if data and "url" in data:
            dog_image_url = data["url"]

            embed = discord.Embed(title="Random Dog Image", color=discord.Color.random())
            embed.set_image(url=dog_image_url)

            await ctx.send(embed=embed)
        else:
            await ctx.send("Failed to fetch dog image.")
    
    @commands.command()
    async def flip(self, ctx):
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"The coin landed on: {result}")