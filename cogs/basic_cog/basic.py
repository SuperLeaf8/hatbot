import discord
from discord.ext import commands
import requests
import random

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # gives the cog a bot instance so we can do bot stuff LOL! ex:    self.bot.name returns bot name
    
    @commands.slash_command()
    async def test(self, ctx: discord.ApplicationContext, bollocks):
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
    

    #test you can delete when finished
    class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
        @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
        async def button_callback(self, button, interaction):
            await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked
    
    @commands.command()
    async def button(self, ctx):
        await ctx.send("hello",view=self.MyView())
    
def setup(bot):
    bot.add_cog(BasicCommands(bot))