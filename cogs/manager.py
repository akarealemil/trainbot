import io
import time
import typing
import base64
import binascii
import re
import datetime
from datetime import datetime
from urllib.parse import quote as urlquote
import psutil
import os

import sys
sys.dont_write_bytecode = True

from utils import *

import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        guilds = len(list(bot.guilds))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        guilds = len(list(self.bot.guilds))
        members = len(set(self.bot.get_all_members()))
        channel = self.bot.get_channel(692753703488192514)

        embed = discord.Embed(colour=discord.Colour.from_rgb(59, 185, 255), title="New Guild")
        embed.add_field(name="Owner", value=f"{guild.owner}", inline=True)
        embed.add_field(name="Owner ID", value=f"{guild.owner.id}", inline=False)
        embed.add_field(name="Guild Name", value=f"{guild}", inline=False)
        embed.add_field(name="Guild ID", value=f"{guild.id}", inline=True)
        embed.add_field(name="Member count", value=f"{guild.member_count}", inline=False)
        await channel.send(embed=embed)

        embedmessage = discord.Embed(colour=discord.Colour.from_rgb(124, 252, 0), title="Welcome - tb!")
        embedmessage.add_field(name="Station Bot Auto Message", value="pls don't hurt me this is an auto message ahh", inline=False)
        embedmessage.add_field(name=f"Hi, {guild.owner}", value=f"hi there, i'm a bot, beep boop. \n\nThis is a message sent regarding the basics of the bot. Thank you for adding me!\n\nWe currently only support the UK, country-wise however we plan on expanding that!", inline=False)
        embedmessage.add_field(name="Getting Started", value="Type **tb!help** for a list of commands. Also, **tb!station** to get information about a station. Pretty cool, ey?")
        embedmessage.add_field(name="Developer", value="beepy boopy. the developer is Emil#0581 - and i hope this message didn't bother you too much! C:")
        await guild.owner.send(embed=embedmessage)


        await self.bot.get_channel(693863811978887180).edit(name=f"Member Count: {members}")
        await self.bot.get_channel(693863787748655104).edit(name=f"Guild Count: {guilds}")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        guilds = len(list(self.bot.guilds))
        members = len(set(self.bot.get_all_members()))
        channel = self.bot.get_channel(692753703488192514)

        embed = discord.Embed(colour=discord.Colour.from_rgb(59, 185, 255), title="Left Guild")
        embed.add_field(name="Owner", value=f"{guild.owner}", inline=True)
        embed.add_field(name="Owner ID", value=f"{guild.owner.id}", inline=False)
        embed.add_field(name="Guild Name", value=f"{guild}", inline=False)
        embed.add_field(name="Guild ID", value=f"{guild.id}", inline=True)
        embed.add_field(name="Member count", value=f"{guild.member_count}", inline=False)
        await channel.send(embed=embed)

        await self.bot.get_channel(693863811978887180).edit(name=f"Member Count: {members}")
        await self.bot.get_channel(693863787748655104).edit(name=f"Guild Count: {guilds}")


def setup(bot):
    bot.add_cog(Manager(bot))
