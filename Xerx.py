from discord.ext import commands
import discord

import asyncio
import random
import asyncpg
import aiohttp
import psutil
from datetime import datetime
import os

import sys
sys.dont_write_bytecode = True

from utils import config

class xerx(commands.Bot):
    def __init__(self):
        super().__init__(
            case_insensitive=True,
            status=discord.Status.online,
            activity=discord.Game(name=f"{config.STATUS}"),
            command_prefix=f"{config.PREFIX}",
            help_command=None
        )

    async def on_ready(self):
        print(f'\n\n\nSYSTEM: We are in {self.guilds} servers!')

    async def start(self):

        cogs = ["cogs.general",
        "cogs.administration.moderation",
        "cogs.administration.handler",
        "cogs.administration.admin",
        "cogs.stations",
        "cogs.manager",]

        for extension in cogs:
            try:
                self.load_extension(extension)
            except BaseException as e:
                print(f"Failed to load {extension}\n{type(e).__name__}: {e}")
        await super().start(config.TOKEN)


if __name__ == "__main__":
    xerx().run()
