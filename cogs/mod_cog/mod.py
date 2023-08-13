import discord
from discord.ext import commands
import datetime

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

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.manage_roles:
            role = discord.utils.get(ctx.guild.roles, id=1072899313312735293)
            if role:
                await member.remove_roles(role)
                await ctx.send(f'{member.mention} has been unmuted.')
            else:
                await ctx.send('Could not find the "Jailed" role. Please make sure the role ID is correct.')
        else:
            await ctx.send('You do not have permission to use this command.')