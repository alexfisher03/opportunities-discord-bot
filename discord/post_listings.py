import discord
from discord.ext import commands, tasks

import datetime
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import util

from datetime import datetime

# UTC time when listings should be posted
times = [datetime.time(hour=12, minute=0, second=0)]

# Posts a formatted message of the listing
async def post_formatted_listing(listing, bot, channel):
    acm_logo = discord.File("acm_logo.png", filename="acm_logo.png")

    # Scrape company logo from Simplify company listing
    has_company_url = listing["company_url"] != ""
    company_logo = None
    if has_company_url:
        soup = BeautifulSoup(requests.get(
            listing["company_url"]).text, 'html.parser')
        img = soup.find(name="img", attrs={"alt": listing["company_name"]})
        company_logo = img["src"]

    # Create embed
    embed = discord.Embed(title=listing["title"], colour=discord.Colour(
        0x5865f2), url=listing["url"], timestamp=datetime.fromtimestamp(listing["date_updated"]))

    embed.set_author(name=listing["company_name"],
                     url=listing["company_url"] if has_company_url else None)
    embed.set_footer(text="Last updated",
                     icon_url=f"attachment://{acm_logo.filename}")

    embed.set_thumbnail(url=company_logo)

    terms = " ".join([f"`{term}`" for term in listing["terms"]])
    embed.add_field(name="Terms 🔎", value=terms, inline=False)

    locations = " ".join(
        [f"`{location}`" for location in listing["locations"]])
    embed.add_field(name="Locations 📌", value=locations, inline=False)

    embed.add_field(name="Sponsorship",
                    value=listing["sponsorship"], inline=False)

    embed.add_field(
        name="Active", value="✅" if listing["active"] else "❌", inline=False)
    
    today = datetime.now().strftime("%A, %B %d, %Y")

    await bot.get_channel(channel).create_thread(
        name=today,
        content=f"# {listing['title']}", 
        embed=embed, 
        files=[acm_logo]
        applied_tags=[]
        )


class PostListings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.post_listings.start()

    def cog_unload(self):
        self.post_listings.cancel()

    @tasks.loop(time=times)
    async def post_listings(self):
        # Get summer listings
        listings = util.getListingsFromJSON()

        util.sortListings(listings)

        summer_listings = util.filterSummer(
            listings, "2025", earliest_date=1710797957)

        # TODO: Figure out how to determine what listings to post


async def setup(bot):
    await bot.add_cog(PostListings(bot))
