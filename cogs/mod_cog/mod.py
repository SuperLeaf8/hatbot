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
    async def mute(self, ctx, member: discord.Member):
        if ctx.author.guild_permissions.administrator:
            await member.timeout_for(datetime.timedelta(days=1))

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