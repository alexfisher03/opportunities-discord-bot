import discord

import os
from dotenv import load_dotenv
load_dotenv()

class Client(discord.Client):
    pass

intents = discord.Intents.default()

client = Client(intents=intents)
client.run(os.getenv("BOT_TOKEN"))