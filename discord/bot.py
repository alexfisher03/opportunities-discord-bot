import asyncio
import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.default()
intents.guilds = True

bot = commands.Bot(command_prefix="", intents=intents)


@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.watching, name="for new opportunities!")
    await bot.change_presence(activity=activity)


async def main():
    await bot.load_extension("setup")
    await bot.load_extension("post_listings")
    await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
