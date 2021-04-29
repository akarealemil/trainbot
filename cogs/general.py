import io
import time
import typing
import base64
import binascii
import asyncio
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

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        guilds = len(list(bot.guilds))

    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    async def help(self, ctx):
        if ctx.author == self.bot.user:
            return
        
        embed=discord.Embed(title="**All Commands**", description=f"**Prefix:** `{config.PREFIX}` \nType `{config.PREFIX}help` to open this menu.", colour=discord.Colour.from_rgb(255,20,147))
        embed.set_author(name="Station Bot")
        embed.add_field(name="**general**", value="`help`, `about`, `botinvite`, `suggest`", inline=False)
        embed.add_field(name="**train**", value="`station`, `stationname`, `crs`, `country`", inline=False)
        embed.add_field(name="**misc**", value="`avatar`, `userinfo`, `guildinfo`, `info`", inline=False)
        embed.set_footer(text='Bot developed by Emil#0581')

        await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    async def about(self, ctx):
        if ctx.author == self.bot.user:
            return

        guilds = len(list(self.bot.guilds))
        
        embed=discord.Embed(colour=discord.Colour.from_rgb(59, 185, 255))
        embed.set_author(name="About Menu")
        embed.add_field(name="**Developer**", value="Emil#0581", inline=False)
        embed.add_field(name="**Library**", value="`discord.py Rewrite`", inline=True)
        embed.add_field(name="**Language**", value="`Python`", inline=True)
        embed.add_field(name="**Servers**", value=f"`{guilds}`", inline=True)
        embed.add_field(name="**Story**", value="This bot is formed apart of Emil's Journey across the UK. He's travelling to every UK Train Station to raise awareness for suicide. This bot will be able to assist him regarding train travel by a lot. This bot will also be developed, in the future, to provide tracking information regarding how many stations have been travelled to etc.", inline=False)
        links = (
        "[Invite](https://discordapp.com/oauth2/authorize?client_id=692740099422683246&scope=bot&permissions=379968) | "
        "[Support](https://discord.gg/dThXJr8) | "
        "[Donate](https://www.patreon.com/m/akarealemil/) | "
        "[Website](https://emil.wtf)"
        )
        embed.add_field(name="**Links**", value=links, inline=False)
        await ctx.channel.send(embed=embed)

    @commands.command(name='userinfo', aliases=['userprofile', 'profile'])
    @commands.cooldown(1,3,type=BucketType.user)
    async def userinfo(self, ctx, *, user: discord.Member = None):
        if ctx.author == self.bot.user:
            return
        
        user = user or ctx.author

        prerole = str(len(user.roles))
        role = int(prerole) - 1
        roles = str(role)
        
        embed = discord.Embed(title=f"Info on {user}", colour=discord.Colour.from_rgb(255,165,0))
        embed.set_author(icon_url=f"{user.avatar_url}", name=f"{user}")
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="ID", value=f"{user.id}", inline=True)
        if user.nick:
            embed.add_field(name="Nickname", value=user.nick, inline=True)
        else:
            embed.add_field(name="Nickname", value="None", inline=True)
        if user.activity:
            activity_type = user.activity.type.name.capitalize()
            embed.add_field(name=activity_type, value=user.activity.name, inline=True)
        else:
            embed.add_field(name="Activity", value="None")
        embed.add_field(name="Created", value=f"{user.created_at.strftime('%d %b %Y, %H:%M')}", inline=True)
        embed.add_field(name="Joined", value=f"{user.joined_at.strftime('%d %b %Y, %H:%M')}", inline=True)
        embed.add_field(name="Status", value=f"""Desktop: {user.desktop_status}
                                            Mobile: {user.mobile_status}""", inline=False)
        if user.roles[1:]:
            roles = ", ".join(role.mention for role in reversed(user.roles[1:20]))
            embed.add_field(name=f"Roles ({prerole})", value=f"{roles}{'...' if len(user.roles) > 20 else ''}", inline=False)
        else:
            embed.add_field(name="Roles", value="None")

        await ctx.channel.send(embed=embed)
    
    @commands.command()
    @commands.cooldown(1,30,type=BucketType.user)
    async def botinvite(self, ctx):
        if ctx.author == self.bot.user:
            return
        embed = discord.Embed(colour=discord.Colour.from_rgb(0,255,0), title="Click Me", url="https://discordapp.com/oauth2/authorize?client_id=692740099422683246&scope=bot&permissions=379968")
        embed.add_field(name="**Invite**", value="Clicking the link above will redirect you to Discord's Bot Invite page! The bot *only* uses the permissions which it requires. No extra permissions are needed.\n\nIf you do not feel comfortable letting the bot make it's own role, make sure the bot has access to the ones listed on the page.")
        await ctx.channel.send(embed=embed)

    @commands.command(name='guildinfo', aliases=['guild_info', 'server_info', 'serverinfo'])
    @commands.cooldown(1,3,type=BucketType.user)
    async def guild_info(self, ctx):
        if ctx.author == self.bot.user:
            return

        guild = ctx.guild
        embed = discord.Embed(colour=discord.Colour.from_rgb(128,0,0), title=f"About: {str(guild)}")

        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="**Owner**", value=f"{guild.owner.mention} | {guild.owner}", inline=True)
        embed.add_field(name="**Created At**", value=f"{guild.created_at.strftime('%d %b %Y, %H:%M')}", inline=True)
        embed.add_field(name="**Channels**", value=f"Voice: {len(guild.voice_channels)}\nText: {len(guild.channels)}", inline=False)
        embed.add_field(name="**Emojis**", value=len(guild.emojis), inline=False)
        embed.add_field(name="**Members**", value=guild.member_count, inline=False)
        embed.add_field(name="**Misc**", value=f"ID: {guild.id} \nRegion: {guild.region} \nVerification Level: {guild.verification_level}", inline=False)

        await ctx.channel.send(embed=embed)
    
    @commands.command()
    @commands.cooldown(1,3,type=BucketType.user)
    async def avatar(self, ctx, *, member: typing.Union[discord.Member, discord.User] = None):
        if ctx.author == self.bot.user:
            return

        member = member or ctx.author
        embed = discord.Embed(colour=discord.Colour.from_rgb(255,255,0))
        embed.set_author(name=str(member), icon_url=str(member.avatar_url_as(format="png", size=32)))
        embed.set_image(url=str(member.avatar_url_as(static_format="png")))
        await ctx.send(embed=embed)
    
    @commands.command(name='suggest', aliases=['suggestion',  'suggests'])
    @commands.cooldown(1,3,type=BucketType.user)
    async def suggestion_cmd(self, ctx, *, suggestion = None):
        if ctx.author == self.bot.user:
            return
        
        guild = ctx.guild

        if suggestion is None:
            embed = discord.Embed(title="", description="Please provide a suggestion to be sent out!")
            await ctx.channel.send(embed=embed)
        else:
 #           file = discord.File(filename="suggestion.png")
            confirmembed = discord.Embed(title="One moment please", description="Your suggestion will be publicly posted in our guild for others to see. Would you like all users to see your Usertag, User ID and Profile Picture, or would you like it to be hidden? \n\nJust a friendly heads up, you will be notified in DMs or via the channel used to send the suggestion whether or not your suggestion has been accepted. \n\n✅ - Yes that is okay. \n❎ - No please keep it private. \n\n**Example:**")
            confirmembed.set_image(url="https://i.imgur.com/CpEfnaG.png")
            confirm = await ctx.send(embed=confirmembed)

            emojis = ['✅', '❎']
            for each_emoji in emojis:
                await confirm.add_reaction(each_emoji)

            def check2(reaction, user):
                return reaction.message.id == confirm.id and user == ctx.author

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
            except asyncio.TimeoutError:
                embederror = discord.Embed(title="CANCELLED", description=f"You didn't react in time!", colour=discord.Colour.from_rgb(255,20,147))
                await ctx.channel.send(embed=embederror)
            else:
                if str(reaction.emoji) == '✅':
                    embed = discord.Embed(title="", description="We have recieved your suggestion and are considering it.")
                    await ctx.send(embed=embed)
                
                    channel = self.bot.get_channel(693503790694793309)
                    
                    embed=discord.Embed(title=f"Suggestion from {ctx.author}")
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    embed.add_field(name="User ID:", value=ctx.author.id, inline=True)
                    embed.add_field(name="Guild:", value=guild, inline=True)
                    embed.add_field(name="Channel:", value=ctx.channel.id)
                    embed.add_field(name="**Suggestion:**", value=suggestion, inline=False)
                    sugembed = await channel.send(embed=embed)

                    await sugembed.add_reaction(":checkmark:700846468659019897")
                    await sugembed.add_reaction(":crossmark:700846468990238820")
                elif str(reaction.emoji) == '❎':
                    embed = discord.Embed(title="", description="We have recieved your suggestion and are considering it. Your information has been removed.")
                    await ctx.send(embed=embed)

                    channel = self.bot.get_channel(693503790694793309)

                    embed=discord.Embed(title=f"Suggestion from Anonymous")
                    embed.add_field(name="Guild:", value=guild, inline=True)
                    embed.add_field(name="Channel:", value=ctx.channel.id)
                    embed.add_field(name="**Suggestion:**", value=suggestion, inline=False)
                    sugembed = await channel.send(embed=embed)

                    await sugembed.add_reaction(":checkmark:700846468659019897")
                    await sugembed.add_reaction(":crossmark:700846468990238820")


    @commands.command(name='info', aliases=['botinfo'])
    @commands.cooldown(1,3,type=BucketType.user)
    async def info_cmd(self, ctx):
        if ctx.author == self.bot.user:
            return
        
        guilds = len(list(self.bot.guilds))
        members = len(set(self.bot.get_all_members()))
        
        embed = discord.Embed(colour=discord.Colour.from_rgb(255,255,0))
        embed.add_field(name="Guilds", value=str(guilds), inline=False)
        embed.add_field(name="Members", value=str(members), inline=False)

        await ctx.send(embed=embed)

    @commands.command(name='country', aliases=['countries'])
    @commands.cooldown(1,3,type=BucketType.user)
    async def country_cmd(self, ctx):
        if ctx.author == self.bot.user:
            return
        

        embed=discord.Embed(colour=discord.Colour.from_rgb(255,255,0))
        embed.add_field(name="Supported Countries", value="UK", inline=False)
        embed.add_field(name="Suggest countries", value="Suggest countries using the `suggest` command! Newsletter coming soon.", inline=False)
        
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
