from discord.ext import commands, tasks

from datetime import datetime, time, timezone, timedelta

import os
import util

TEST_MODE = os.getenv("TEST_MODE") == "True"

times = [time(hour=12, minute=0, second=0)] # Post listings daily at 12:00 UTC

class PostListings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if TEST_MODE:
            self.posted_today = False

        self.post_listings.start()

    def cog_unload(self):
        self.post_listings.cancel()

    # @tasks.loop(time=times) Use this for Production, discord does not allow mixing relative and explicit times 
    @tasks.loop(seconds=10)
    async def post_listings(self):
        if TEST_MODE and self.posted_today:
            return

        if TEST_MODE:
            # Use hardcoded sample listings for testing
            listings = [
                {
                    "title": "Software Engineer Intern",
                    "company_name": "Acme Corp",
                    "company_url": "https://www.acme.com",
                    "url": "https://www.acme.com/jobs/123",
                    "date_posted": datetime.now(timezone.utc).timestamp(),
                    "date_updated": datetime.now(timezone.utc).timestamp(),
                    "locations": ["San Francisco, CA", "Remote"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "Yes",
                    "active": True,
                    "is_visible": True
                },
                {
                    "title": "Data Analyst Intern",
                    "company_name": "Globex Inc",
                    "company_url": "https://www.globex.com",
                    "url": "https://www.globex.com/careers/456",
                    "date_posted": datetime.now(timezone.utc).timestamp(),
                    "date_updated": datetime.now(timezone.utc).timestamp(),
                    "locations": ["New York, NY"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "No",
                    "active": True,
                    "is_visible": True
                },
            ]
        else:
            # Get listings from JSON file
            listings = util.getDataFromJSON("listings.json")
            util.sortListings(listings)

        # Create the message content
        content = ""
        for listing in listings:
            # Format each listing
            content += f"**{listing['title']}** at **{listing['company_name']}**\n"
            content += f"Locations: {', '.join(listing['locations'])}\n"
            content += f"Terms: {', '.join(listing['terms'])}\n"
            content += f"Sponsorship: {listing['sponsorship']}\n"
            content += f"Active: {'✅' if listing['active'] else '❌'}\n"
            content += f"Link: {listing['url']}\n\n"

        # Determine the season and format the thread title
        now = datetime.now()
        month = now.month
        day = now.day
        year_short = now.strftime("%y")  # Last two digits of the year

        if 8 <= month <= 12:
            season = "FALL"
        elif 1 <= month <= 5:
            season = "SPRING"
        elif 6 <= month <= 7:
            season = "SUMMER"
        else:
            season = "UNKNOWN" # should be unreachable, maybe assert?

        thread_title = f"{season} {year_short}: {month_name} {day}"

        # Post the message in each guild's forum channel as a new thread
        existing_guilds = util.getDataFromJSON("guilds.json")
        for guild in existing_guilds:
            forum_channel = self.bot.get_channel(guild['channel'])
            
            # Create a new thread with the formatted title
            await forum_channel.create_thread(
                name=thread_title,
                content=content
            )
        
        # Log number of listings posted in number of guilds
        print(f"Posted {len(listings)} listings in {len(existing_guilds)} guilds on {month_name} {day}")
        
        if TEST_MODE:
            self.posted_today = True

    @post_listings.before_loop
    async def before_post_listings(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(PostListings(bot))
