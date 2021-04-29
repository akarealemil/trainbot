import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

import asyncio

import sys
sys.dont_write_bytecode = True

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, *, user: discord.Member = None, reason = None):
        if ctx.author == self.bot.user:
            return
        
        if user is None:
            embed = discord.Embed(title="", description=":warning: You need to provide a user! :warning:")
            await ctx.channel.send(embed=embed)
        elif reason is None:
            reason = "No reason"
        else:
            await user.send(f"You have been kicked from {ctx.message.guild.name} for {reason}!")
            await self.bot.kick(user, reason = f"[KICK] {user.id} for {reason}")
            
            embed = discord.Embed(title="", description=f":warning: The user {user} has been kicked! :warning:")
            await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.Member, *, reason=None):
        if ctx.author == self.bot.user:
            return
        if reason is None:
            reason = "No reason"

        await ctx.guild.ban(user, reason=f"[SOFTBAN] {user.id} for {reason}")
        await ctx.guild.unban(user, reason=f"[SOFTBAN UNBAN]")

        await ctx.channel.send(f"Softbanned {user} for {reason}")

    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        if ctx.author == self.bot.user:
            return
        if reason is None:
            reason = "No reason"

        await ctx.guild.ban(
            discord.Object(id=user), reason=f"[BAN] {user} for {reason}"
        )
        await ctx.channel.send(f"Banned {user} for {reason}")

    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.Member, *, reason=None):
        if ctx.author == self.bot.user:
            return
        if reason is None:
            reason = "No reason"

        await ctx.guild.unban(
            discord.Object(id=user), reason=f"[UNBAN] {user} for {reason}"
        )
        await ctx.channel.send(f"Unbanned {user} for {reason}")

    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def lock(self, ctx, *, reason=None):
        if ctx.author == self.bot.user:
            return

        if reason is None:
            reason = "No reason"

        guild = ctx.author.guild 

        await ctx.channel.set_permissions(guild.default_role, send_messages=False)
        embed = discord.Embed(title="**Channel Locked**", description=f"This channel has been locked! \n\nReason: {reason}", colour=discord.Colour.from_rgb(255,20,147))
        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def unlock(self, ctx):
        if ctx.author == self.bot.user:
            return

        guild = ctx.author.guild 

        await ctx.channel.set_permissions(guild.default_role, send_messages=True)
        embed = discord.Embed(title="**Channel Unlocked**", description="This channel has been unlocked!", colour=discord.Colour.from_rgb(255,20,147))
        await ctx.channel.send(embed=embed)

    @commands.command(aliases=['purge', 'clear'])
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1,3,type=BucketType.user)
    async def prune(self, ctx, num: int, target: discord.Member=None):
        if ctx.author == self.bot.user:
            return
        if num > 500 or num < 0:
            return await ctx.send("Invalid amount. Maximum is 500.")
        num = num + 1
        deleted = await ctx.channel.purge(limit=num)

        embed = discord.Embed(title="**Purged Messages**", description=f"I have deleted **{len(deleted)}/{num}** messages for you!", colour=discord.Colour.from_rgb(255,20,147))
        await ctx.channel.send(embed=embed, delete_after=30)

    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, say = None):
        if ctx.author == self.bot.user:
            return
        if say is None:
            embed = discord.Embed(title="", description="You need to tell me to say something, for me to say it!")
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send(f"{say}")

    @commands.command()
    @commands.cooldown(1,10,type=BucketType.user)
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, *, rolename= None):
        guild = ctx.guild
        if ctx.author == self.bot.user:
            return
        if rolename is None:
            embed = discord.Embed(title="", description="You need to give me a role name! \nExample:x-createrole [RoleName]")
            await ctx.channel.send(embed=embed)
        else:
            await guild.create_role(name=f"{rolename}")
            await ctx.channel.send(f"I have successfully created your role called, {rolename}")

    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, target: discord.Member=None):
        guild = ctx.guild
        if ctx.author == self.bot.user:
            return

        role = discord.utils.get(self, ctx.guild.roles, name="Muted")

        overwrite = discord.PermissionOverwrite()
        #overwrite.send_messages = False
        #overwrite.read_messages = True

        if target is None:
            await ctx.channel.send("Please specify a user!")
            if role is None:
                await guild.create_role(name="Muted")
                await ctx.channel.send("I did not find a 'Muted' role, so instead I created one for you. Do not remove this role!")
                await ctx.channel.set_permissions(target, overwrite=overwrite)

        if role is None:
            await guild.create_role(name="Muted")
            await ctx.channel.send("I did not find a 'Muted' role, so instead I created one for you. Do not remove this role!")
            await target.add_roles(role)
            await ctx.channel.set_permissions(target, overwrite=overwrite)
            embed = discord.Embed(title="**Muted**", description=f"The user {target} has been muted!", colour=discord.Colour.from_rgb(255,20,147))
            await ctx.channel.send(embed=embed)
        else:
            await target.add_roles(role)
            await ctx.channel.set_permissions(target, overwrite=overwrite)
            embed = discord.Embed(title="**Muted**", description=f"The user {target} has been muted!", colour=discord.Colour.from_rgb(255,20,147))
            await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, target: discord.Member=None):

        if ctx.author == self.bot.user:
            return

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        overwrite = discord.PermissionOverwrite()
        #overwrite.send_messages = True
        #overwrite.read_messages = True

        if target is None:
            await ctx.channel.send("Please specify a user!")

        if role is None:
            await guild.create_role(name="Unmuted")
            await ctx.channel.send("I did not find a 'Muted' role, so instead I created one for you. Do not remove this role!")
            await target.remove_roles(role)
            await ctx.channel.set_permissions(target, overwrite=overwrite)
            embed = discord.Embed(title="**Unmuted**", description=f"The user {target} has been muted!", colour=discord.Colour.from_rgb(255,20,147))
            await ctx.channel.send(embed=embed)
        else:
            await target.remove_roles(role)
            await ctx.channel.set_permissions(target, overwrite=overwrite)
            embed = discord.Embed(title="**Unmuted**", description=f"The user {target} has been muted!", colour=discord.Colour.from_rgb(255,20,147))
            await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,5,type=BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def announce(self, ctx, announcechannel: discord.TextChannel = None, title = None, *, description = None):
        
        if ctx.author == self.bot.user:
            return
        
        if announcechannel is None:
            embed = discord.Embed(title="", description=":warning: You need to provide a channel! :warning:")
            await ctx.channel.send(embed=embed)
        elif title is None:
            embed = discord.Embed(title="", description=":warning: You need to provide a title! :warning:")
            await ctx.channel.send(embed=embed)
        else:
            await ctx.send("Your announcement has been posted")

            embed = discord.Embed(title=f"{title}", description=f"{description}")
            await announcechannel.send(embed=embed)

    @commands.command(aliases=["nick", "nickname", "changenick"])
    @commands.cooldown(1,10,type=BucketType.user)
    @commands.has_permissions(manage_nicknames=True)
    async def setnick(self, ctx, member: discord.Member = None, *, nick = None):
        if ctx.author == self.bot.user:
            return
        if member is None:
            member == ctx.author
        if nick is None:
            await ctx.send("Please provide a nickname")
        else:
            await member.edit(nick=nick)
            await ctx.send("nick edited")

    @commands.command(aliases=["sm"])
    @commands.cooldown(1,30,type=BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, amount: int = None):
        if ctx.author == self.bot.user:
            return

        if amount is None:
            await ctx.send("Please provide a number to slowmode!")
        elif amount > 21600:
            await ctx.send("That number is larger than the allowed limit for slowmode on Discord! Please try a lower number")
        elif amount == 0:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send("Slowmode disabled")
        else:
            await ctx.channel.edit(slowmode_delay=amount)
            await ctx.send("slowmode enabled")

    @commands.command()
    @commands.cooldown(1,10,type=BucketType.user)
    @commands.has_permissions(deafen_members=True)
    async def deafen(self, ctx, member: discord.Member = None, *, reason = None):
        
        if reason is None:
            reason = "No reason"
        
        if member is None:
            await ctx.send("Please provide a user to deafen!")
        if member.voice is None:
            await ctx.send("User is not connected to a voice channel!")
        else:
            await member.edit(deafen=True, reason=reason)
            await ctx.send("User deafened")

    @commands.command()
    @commands.cooldown(1,30,type=BucketType.user)
    @commands.has_permissions(deafen_members=True)
    async def punish(self, ctx, member: discord.Member = None):
                
        if member is None:
            await ctx.send("Please provide a user to punish!")
        
        else:
            embed = discord.Embed(title="**PUNISH GUI**", description="If you want to punish somebody this is the way! \n\n:warning: Will warn the user provided \n:hammer: Will kick the user provided \n:wave: Will ban the user provided")
            message = await ctx.send(embed=embed)
            await message.add_reaction("\U000026a0")
            await message.add_reaction("\U0001f528")
            await message.add_reaction("\U0001f44b")


def setup(bot):
    bot.add_cog(Moderation(bot))
