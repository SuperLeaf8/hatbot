import discord
from discord.ext import commands
import datetime
import asyncio
import random

class ModCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await ctx.send(f'Banned {member.mention}')
        else:
            await ctx.send('You do not have permission to use this command.')

    @commands.command()
    async def unban(self, ctx, user_id: int, *, reason="No reason provided."):
        #Unban a user by ID
        user = await self.bot.fetch_user(user_id)
        if user:
            await ctx.guild.unban(user, reason=reason)
            await ctx.send(f"{user.name} has been unbanned.")
        else:
            await ctx.send("User not found.")

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            await ctx.send(f'Kicked {member.mention}')
        else:
            await ctx.send('You do not have permission to use this command.')

    @commands.command()
    async def mute(self, ctx, member: discord.Member, duration="1d", *, reason="No reason lol"):
        # time = duration.split(" ")[0] # get the FIRST time duration
        time = duration
        timedeltas = {
            "weeks": 0,
            "days": 0,
            "hours": 0,
            "minutes": 0
        }

        try: # check if duration format is proper
            magnitude = int(time[:-1])
        except ValueError:
            await ctx.respond("Not valid duration format")
            return
        
        match time[-1]:
            case "w":
                timedeltas["weeks"] = magnitude
            case "d":
                timedeltas["months"] = magnitude
            case "h":
                timedeltas["hours"] = magnitude
            case "m":
                timedeltas["minutes"] = magnitude
            case _:
                await ctx.respond("Not valid duration unit")
                return

        if ctx.author.guild_permissions.administrator:
            await member.timeout_for(
                duration=datetime.timedelta(
                    weeks=timedeltas["weeks"],
                    days=timedeltas["days"],
                    hours=timedeltas["hours"],
                    minutes=timedeltas["minutes"],
                    ),
                reason=reason
                )
            await ctx.send(f'{member.mention} has been muted.')

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.administrator:
            await member.remove_timeout()
            await ctx.send(f'{member.mention} has been unmuted.')
        else:
            await ctx.send('User is not muted.')
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, messages: int):
        z = await ctx.channel.purge(limit=messages+1)
        msg = await ctx.send(f"{str(len(z)-1)} messages purged!")
        await asyncio.sleep(3)
        await msg.delete()