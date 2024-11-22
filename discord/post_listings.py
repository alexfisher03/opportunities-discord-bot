from discord.ext import commands, tasks

from datetime import datetime, time, timezone, timedelta

from asyncio import TimeoutError, wait_for

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
            
            # Sort listings for those only appearing since the day prior
            now = datetime.now()
            yesterday = now - timedelta(days=1)
            yesterday_midnight = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
            listings = util.filterSummer(listings, str(yesterday.year + 1), earliest_date=int(yesterday_midnight.timestamp()))
        
        # Log no listings received for that day
        now = datetime.now()
        month = now.month
        month_name = now.strftime("%B")  # Full month name
        day = now.day
        year_short = now.strftime("%y")  # Last two digits of the year
        
        if len(listings) == 0:
            print(f"No listings posted on {month_name} {day}")
            return


        
        #create messages list so the split content is smooth
        messages = []
        MESSAGE_LIMIT = 2000
        # Create the message content
        # TODO: Split content into separate messages if length too large
        content = ""
        for listing in listings:
            temp_content = ""
            # Format each listing
            temp_content += f"# {listing['title']} at {listing['company_name']}\n"
            temp_content += f"**Locations:** {' '.join([f'`{l}`' for l in listing['locations']])}\n"
            temp_content += f"**Terms:** {' '.join([f'`{t}`' for t in listing['terms']])}\n"
            temp_content += f"**Sponsorship:** {listing['sponsorship']}\n"
            temp_content += f"**Link:** {listing['url']}\n\n" 

            if len(content) + len(temp_content) > MESSAGE_LIMIT:
                messages.append(content)
                content = temp_content

            else:
                content += temp_content

        #checks to see if there is content remaining
        if content.strip():
            messages.append(content)




        # Determine the season and format the thread title
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

            # Create the thread
            try:
                thread = await forum_channel.create_thread(
                    name=thread_title,
                    content=messages[0]  # Use the first message to create the thread
                )
            except Exception as e:
                print(f"Failed to create thread: {e}")
                return
            
            await asyncio.sleep(1)  # Add a 1-second delay between messages

            # Post the rest of the messages in the thread
            for msg in messages[1:]:
                try:
                    await thread.send(msg)
                except Exception as e:
                    print(f"Failed to send message in thread {thread.name}: {e}")           
             
         # Log number of listings posted in number of guilds
        print(f"Posted {len(listings)} listings in {len(existing_guilds)} guilds on {month_name} {day}")
        
        if TEST_MODE:
            self.posted_today = True

    @post_listings.before_loop
    async def before_post_listings(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(PostListings(bot))
