import discord
from discord.ext import commands
import asyncio

TOKEN = "BOT_TOKEN"

# Initialize the bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Run the bot and load the cog
async def main():
    await bot.load_extension("post_listings")  # Make sure your file is named `post_listings.py`
    await bot.start(TOKEN)

asyncio.run(main())
