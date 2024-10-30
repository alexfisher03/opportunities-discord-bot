import asyncio
import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="", intents=intents)


async def main():
    await bot.load_extension("post_listings")
    await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
