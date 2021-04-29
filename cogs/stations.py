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
import asyncio
import csv
import requests

import sys
sys.dont_write_bytecode = True

from utils import *

import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class Stations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        guilds = len(list(bot.guilds))

    @commands.command(name='station', aliases=['stations', 'stationz'])
    @commands.cooldown(1,5,type=BucketType.user)
    async def station_command(self, ctx, *, stationinput = None):
        if ctx.author == self.bot.user:
            return
        
        now = datetime.now()
        dt_string = now.strftime("%H:%M")

        auth = ('rttapi_ayyitsemil', 'bf27d67e6f7057bc9e89c42c7d72cf1051ad4a06')

        def check50(m):
            return ctx.author == m.author


        if stationinput is None:

            embedmain1 = discord.Embed(title="Welcome", description="""Welcome to the Station Information Control. You selected this to display information regarding a given station. Firstly, provide me with a station. Make sure it's not closed!""", colour=discord.Colour.from_rgb(255,20,147))
            embedmain1.add_field(name="Notice", value="Please enter a station name, for example 'London Euston' or the CRS Code, for example EUS. If you enter it incorrectly, it may give an error!")
            mainembed1 = await ctx.channel.send(embed=embedmain1)

            try:
                msg = await self.bot.wait_for('message', timeout=60.0, check=check50)
                msg = msg.content.lower()
                
                with open('TS.csv', "r") as tlist:
                    stlist = csv.reader(tlist)
                    for row in stlist:
                        found = False
                        if msg in (row[0].lower(), row[1].lower()):

                            found = True
                            
                            dept = f'https://api.rtt.io/api/v1/json/search/{row[1]}'
                            arri = f'https://api.rtt.io/api/v1/json/search/{row[1]}/arrivals'

                            embedmain2 = discord.Embed(title="Welcome", description="""Thank you for providing the Station Name. I've retrieved the station, please select one of these options""", colour=discord.Colour.from_rgb(255,20,147))
                            embedmain2.add_field(name=":watch: ARRIVALS", value="Select this if you want ARRIVALS to display", inline=False)
                            embedmain2.add_field(name=":timer: DEPARTURES", value="Select this if you want DEPARTURES to display", inline=False)
                            embedmain2.add_field(name=":stopwatch: BOTH", value="Select this if you want BOTH (depatures and arrivals) to display", inline=False)
                            embedmain2.add_field(name="WARNING", value="There may be a maximum of 5 depatures OR arrivals posted (Maximum of 10 embeds)", inline=False)
                            embedmain2.add_field(name="Notice", value="For smaller stations, Arrivals and Departures may show the SAME information. For larger stations it may be different as the trains arriving may be terminating there, whilst departing trains may be going on further!")

                            mainembed = await ctx.send(embed=embedmain2)

                            emojis = ['⌚', '⏲️', '⏱️']
                            for each_emoji in emojis:
                                await mainembed.add_reaction(each_emoji)
                            
                            def check2(reaction, user):
                                return reaction.message.id == mainembed.id and user == ctx.author

                            try:
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
                            except asyncio.TimeoutError:
                                embederror = discord.Embed(title="CANCELLED", description=f"Your attention please. We are sorry that the {dt_string}, Train Information Bot service to Destination/Arrival Input has been cancelled. This is due to your lack of emoji choice. The Developer apologises for the inconvenience this may cause you.", colour=discord.Colour.from_rgb(255,20,147))
                                await ctx.channel.send(embed=embederror)
                            else:

                                try:
                                    with requests.Session() as s:

                                        depar = s.get(dept, auth=auth)
                                        obtaindata = depar.json()

                                        arriv = s.get(arri, auth=auth)
                                        arrivdata = arriv.json()

                                        for i in range(1,4):

                                            toc = obtaindata["services"][i]['atocName']
                                            deptime = obtaindata["services"][i]['locationDetail']['gbttBookedDeparture']
                                            accdeptime = obtaindata["services"][i]['locationDetail']['realtimeDeparture']
                                            destin = obtaindata["services"][i]['locationDetail']['destination'][0]["description"]
                                            destatime = obtaindata["services"][i]['locationDetail']['destination'][0]['publicTime']
                                            try:
                                                status = obtaindata["services"][i]['locationDetail']['serviceLocation']
                                            except (KeyError):
                                                status = "Not Confirmed"

                                            toc2 = arrivdata["services"][i]['atocName']
                                            origin = arrivdata["services"][i]['locationDetail']['origin'][0]["description"]
                                            odeptime = arrivdata["services"][i]['locationDetail']['origin'][0]["publicTime"]
                                            destatime2 = arrivdata["services"][i]['locationDetail']['destination'][0]['publicTime']

                                            if str(reaction.emoji) == '⌚':
                                                aembed2=discord.Embed(title="ARRIVALS", description=f"", colour=discord.Colour.from_rgb(255,20,147))
                                                aembed2.set_author(name=f"STATION ARRIVALS | Station {msg}")
                                                aembed2.add_field(name="TOC (Train Operating Company)", value=f"{toc2}", inline=True)
                                                aembed2.add_field(name="Arrival Time", value=f"{destatime2}", inline=True)
                                                aembed2.add_field(name="Origin", value=f"{origin}", inline=True)
                                                aembed2.add_field(name="Origin Departure Time", value=f"{odeptime}", inline=True)
                                                aembed2.set_footer(text='Bot developed by Emil#0581')

                                                await ctx.send(embed=aembed2)
                                            
                                            elif str(reaction.emoji) == '⏲️':

                                                embed2=discord.Embed(title="DEPATURES", description=f"", colour=discord.Colour.from_rgb(255,20,147))
                                                embed2.set_author(name=f"STATION DEPARTURES | Station {msg}")
                                                embed2.add_field(name="TOC (Train Operating Company)", value=f"{toc}", inline=True)
                                                embed2.add_field(name="Departure Time", value=f"{deptime}", inline=True)
                                                embed2.add_field(name="Destination", value=f"{destin}", inline=True)
                                                embed2.add_field(name="Destination Arrival Time", value=f"{destatime}", inline=True)
                                                embed2.add_field(name="Actual Departure Time", value=f"{accdeptime}", inline=True)
                                                embed2.add_field(name="Status", value=f"{status}", inline=True)
                                                embed2.set_footer(text='Bot developed by Emil#0581')

                                                await ctx.send(embed=embed2)
                                            
                                            elif str(reaction.emoji) == '⏱️':
                                                aembed2=discord.Embed(title="ARRIVALS", description=f"", colour=discord.Colour.from_rgb(255,20,147))
                                                aembed2.set_author(name=f"STATION ARRIVALS | Station {msg}")
                                                aembed2.add_field(name="TOC (Train Operating Company)", value=f"{toc2}", inline=True)
                                                aembed2.add_field(name="Arrival Time", value=f"{destatime2}", inline=True)
                                                aembed2.add_field(name="Origin", value=f"{origin}", inline=True)
                                                aembed2.add_field(name="Origin Departure Time", value=f"{odeptime}", inline=True)
                                                aembed2.set_footer(text='Bot developed by Emil#0581')

                                                await ctx.send(embed=aembed2)

                                                dembed2=discord.Embed(title="DEPATURES", description=f"", colour=discord.Colour.from_rgb(255,20,147))
                                                dembed2.set_author(name=f"STATION DEPARTURES | Station {msg}")
                                                dembed2.add_field(name="TOC (Train Operating Company)", value=f"{toc}", inline=True)
                                                dembed2.add_field(name="Departure Time", value=f"{deptime}", inline=True)
                                                dembed2.add_field(name="Destination", value=f"{destin}", inline=True)
                                                dembed2.add_field(name="Destination Arrival Time", value=f"{destatime}", inline=True)
                                                dembed2.add_field(name="Actual Departure Time", value=f"{accdeptime}", inline=True)
                                                dembed2.add_field(name="Status", value=f"{status}", inline=True)
                                                dembed2.set_footer(text='Bot developed by Emil#0581')

                                                await ctx.send(embed=dembed2)

                                except (ConnectionError, TimeoutError):
                                    await ctx.send("If you are seeing this error, either one of two things has happened: API is down on RealTrainTimes, NetworkRail or similar. OR there's no more trains on this day and you'd need to wait until morning for it to update. Information is obtained from NR API, so it's whenever they update it")
                                    time.sleep(600)
                                except Exception as e:
                                    await ctx.send(e)
                                    await ctx.send("Please report this to the owner using tb!suggestion error, and include your discord invite link!")
                            
                            break

                    else:
                        await ctx.send("This station could not be found. Retry the command.")


            except asyncio.TimeoutError:
                embederror2 = discord.Embed(title="CANCELLED", description=f"Your attention please. We are sorry that the {dt_string}, Train Information Bot service to Station Name Input has been cancelled. This is due to your lack of response. The Developer apologises for the inconvenience this may cause you.", colour=discord.Colour.from_rgb(255,20,147))
                
                await ctx.send(embed=embederror2)

        else:
            stationinput = stationinput.lower()
            with open('TS.csv', "r") as tlist:
                stlist = csv.reader(tlist)
                for row in stlist:
                    if stationinput in (row[0].lower(), row[1].lower()):

                        dept = f'https://api.rtt.io/api/v1/json/search/{row[1]}'
                        arri = f'https://api.rtt.io/api/v1/json/search/{row[1]}/arrivals'

                        embedmain2 = discord.Embed(title="Welcome", description="""Thank you for providing the Station Name. I've retrieved the station, please select one of these options""", colour=discord.Colour.from_rgb(255,20,147))
                        embedmain2.add_field(name=":watch: ARRIVALS", value="Select this if you want ARRIVALS to display", inline=False)
                        embedmain2.add_field(name=":timer: DEPARTURES", value="Select this if you want DEPARTURES to display", inline=False)
                        embedmain2.add_field(name=":stopwatch: BOTH", value="Select this if you want BOTH (depatures and arrivals) to display", inline=False)
                        embedmain2.add_field(name="WARNING", value="There may be a maximum of 5 depatures OR arrivals posted (Maximum of 10 embeds)", inline=False)
                        embedmain2.add_field(name="Notice", value="For smaller stations, Arrivals and Departures may show the SAME information. For larger stations it may be different as the trains arriving may be terminating there, whilst departing trains may be going on further!")

                        mainembed = await ctx.send(embed=embedmain2)

                        emojis = ['⌚', '⏲️', '⏱️']
                        for each_emoji in emojis:
                            await mainembed.add_reaction(each_emoji)
                        
                        def check2(reaction, user):
                            return reaction.message.id == mainembed.id and user == ctx.author

                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check2)
                        except asyncio.TimeoutError:
                            embederror = discord.Embed(title="CANCELLED", description=f"Your attention please. We are sorry that the {dt_string}, Train Information Bot service to Destination/Arrival Input has been cancelled. This is due to your lack of emoji choice. The Developer apologises for the inconvenience this may cause you.", colour=discord.Colour.from_rgb(255,20,147))
                            await ctx.channel.send(embed=embederror)
                        else:

                            try:
                                with requests.Session() as s:

                                    depar = s.get(dept, auth=auth)
                                    obtaindata = depar.json()

                                    arriv = s.get(arri, auth=auth)
                                    arrivdata = arriv.json()

                                    for i in range(1,4):

                                        toc = obtaindata["services"][i]['atocName']
                                        deptime = obtaindata["services"][i]['locationDetail']['gbttBookedDeparture']
                                        accdeptime = obtaindata["services"][i]['locationDetail']['realtimeDeparture']
                                        destin = obtaindata["services"][i]['locationDetail']['destination'][0]["description"]
                                        destatime = obtaindata["services"][i]['locationDetail']['destination'][0]['publicTime']
                                        try:
                                            status = obtaindata["services"][i]['locationDetail']['serviceLocation']
                                        except (KeyError):
                                            status = "Not Confirmed"

                                        toc2 = arrivdata["services"][i]['atocName']
                                        origin = arrivdata["services"][i]['locationDetail']['origin'][0]["description"]
                                        odeptime = arrivdata["services"][i]['locationDetail']['origin'][0]["publicTime"]
                                        destatime2 = arrivdata["services"][i]['locationDetail']['destination'][0]['publicTime']

                                        if str(reaction.emoji) == '⌚':
                                            aembed2=discord.Embed(title="ARRIVALS", description=f"", colour=discord.Colour.from_rgb(255,20,147))
                                            aembed2.set_author(name=f"STATION ARRIVALS | Station {stationinput}")
                                            aembed2.add_field(name="TOC (Train Operating Company)", value=f"{toc2}", inline=True)
                                            aembed2.add_field(name="Arrival Time", value=f"{destatime2}", inline=True)
                                            aembed2.add_field(name="Origin", value=f"{origin}", inline=True)
                                            aembed2.add_field(name="Origin Departure Time", value=f"{odeptime}", inline=True)
                                            aembed2.set_footer(text='Bot developed by Emil#0581')

                                            await ctx.send(embed=aembed2)
                                        
                                        elif str(reaction.emoji) == '⏲️':

                                            embed2=discord.Embed(title="DEPATURES", description=f"", colour=discord.Colour.from_rgb(255,20,147))
                                            embed2.set_author(name=f"STATION DEPARTURES | Station {stationinput}")
                                            embed2.add_field(name="TOC (Train Operating Company)", value=f"{toc}", inline=True)
                                            embed2.add_field(name="Departure Time", value=f"{deptime}", inline=True)
                                            embed2.add_field(name="Destination", value=f"{destin}", inline=True)
                                            embed2.add_field(name="Destination Arrival Time", value=f"{destatime}", inline=True)
                                            embed2.add_field(name="Actual Departure Time", value=f"{accdeptime}", inline=True)
                                            embed2.add_field(name="Status", value=f"{status}", inline=True)
                                            embed2.set_footer(text='Bot developed by Emil#0581')

                                            await ctx.send(embed=embed2)
                                        
                                        elif str(reaction.emoji) == '⏱️':
                                            aembed2=discord.Embed(title="ARRIVALS", description=f"", colour=discord.Colour.from_rgb(255,20,147))
                                            aembed2.set_author(name=f"STATION ARRIVALS | Station {stationinput}")
                                            aembed2.add_field(name="TOC (Train Operating Company)", value=f"{toc2}", inline=True)
                                            aembed2.add_field(name="Arrival Time", value=f"{destatime2}", inline=True)
                                            aembed2.add_field(name="Origin", value=f"{origin}", inline=True)
                                            aembed2.add_field(name="Origin Departure Time", value=f"{odeptime}", inline=True)
                                            aembed2.set_footer(text='Bot developed by Emil#0581')

                                            await ctx.send(embed=aembed2)

                                            dembed2=discord.Embed(title="DEPATURES", description=f"", colour=discord.Colour.from_rgb(255,20,147))
                                            dembed2.set_author(name=f"STATION DEPARTURES | Station {stationinput}")
                                            dembed2.add_field(name="TOC (Train Operating Company)", value=f"{toc}", inline=True)
                                            dembed2.add_field(name="Departure Time", value=f"{deptime}", inline=True)
                                            dembed2.add_field(name="Destination", value=f"{destin}", inline=True)
                                            dembed2.add_field(name="Destination Arrival Time", value=f"{destatime}", inline=True)
                                            dembed2.add_field(name="Actual Departure Time", value=f"{accdeptime}", inline=True)
                                            dembed2.add_field(name="Status", value=f"{status}", inline=True)
                                            dembed2.set_footer(text='Bot developed by Emil#0581')

                                            await ctx.send(embed=dembed2)

                            except (ConnectionError, TimeoutError):
                                await ctx.send("If you are seeing this error, either one of two things has happened: API is down on RealTrainTimes, NetworkRail or similar. OR there's no more trains on this day and you'd need to wait until morning for it to update. Information is obtained from NR API, so it's whenever they update it")
                                time.sleep(600)

                            except Exception as e:
                                print(e)
                                await ctx.send("If you are seeing this error, the API is down.")
                        
                        break

                else:
                    await ctx.send("This station could not be found. Retry the command.")

    @commands.command(name='name', aliases=['stationconvert', 'stationcrs', 'CRS', 'crscode', 'crsstation'])
    @commands.cooldown(1,5,type=BucketType.user)
    async def name_command(self, ctx, *, station = None):
        if ctx.author == self.bot.user:
            return
        
        now = datetime.now()
        dt_string = now.strftime("%H:%M")

        if station is None:

            embedmain1 = discord.Embed(title="Welcome", description="""Welcome to the Station <-> CRS. You selected this to obtain a CRS code from a station, or a station from a CRS code""", colour=discord.Colour.from_rgb(255,20,147))
            mainembed1 = await ctx.channel.send(embed=embedmain1)

            def check50(m):
                return ctx.author == m.author

            msg = await self.bot.wait_for('message', timeout=60.0, check=check50)
            msg = msg.content.lower()

            with open('TS.csv', "r") as tlist:
                stlist = csv.reader(tlist)
                for row in stlist:
                    if msg in (row[0].lower(), row[1].lower()):
                        crsembed = discord.Embed(title=f"Station CRS - {row[1]}", description=f"**{row[0]}** is the corresponding station to the inputted CRS Code")
                        await ctx.send(embed=crsembed)
                        break
                else:
                    await ctx.send('This station is not apart of the list.')
        
        else:
            station = station.lower()
            with open('TS.csv', "r") as tlist:
                stlist = csv.reader(tlist)
                for row in stlist:
                    if msg in (row[0].lower(), row[1].lower()):
                        crsembed = discord.Embed(title=f"Station CRS - {row[1]}", description=f"**{row[0]}** is the corresponding station to the inputted CRS Code")
                        await ctx.send(embed=crsembed)
                        break
                else:
                    await ctx.send('This station is not apart of the list.')



def setup(bot):
    bot.add_cog(Stations(bot))
