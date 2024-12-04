import asyncio
import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True  # Ensure this is enabled

bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    try:
        activity = discord.Activity(
            type=discord.ActivityType.watching, name="for new opportunities!")
        await bot.change_presence(activity=activity)
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    except Exception as e:
        if bot.user.id == 0:
            print('Could not connect to channel. Make sure the token is valid.')
        if bot.user is None:
            print('Could not connect to ACMConnect bot user. Make sure the token is valid.')

async def main():
    await bot.load_extension("setup")
    await bot.load_extension("post_listings")
    await bot.start(os.getenv("BOT_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
