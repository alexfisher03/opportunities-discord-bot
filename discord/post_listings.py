import discord
from discord.ext import commands, tasks
from datetime import datetime, time
import os
import util

# Set TEST_MODE to True for testing (loads dummy data)
TEST_MODE = os.getenv("TEST_MODE") == "True"

# Define times for the loop (use 12:00 UTC daily for production)
times = [time(hour=12, minute=0, second=0)] if not TEST_MODE else None


class PostListings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.posted_today = False  # Prevent multiple posts in TEST_MODE
        self.post_listings.start()

    def cog_unload(self):
        print("Unloading cog. Stopping post_listings loop.")
        self.post_listings.cancel()

    @tasks.loop(time=times) if not TEST_MODE else tasks.loop(minutes=1)
    async def post_listings(self):
        """Posts job listings to the specified channel."""
        if TEST_MODE and self.posted_today:
            print("Skipping post: already posted today in TEST_MODE.")
            return

        print("Running post_listings loop...")

        # Load data
        if TEST_MODE:
            listings = [
                {
                    "title": "Software Engineer Intern",
                    "company_name": "Acme Corp",
                    "company_url": "https://www.acme.com",
                    "url": "https://www.acme.com/jobs/123",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["San Francisco, CA", "Remote"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "Yes",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Data Analyst Intern",
                    "company_name": "Data Inc.",
                    "company_url": "https://www.datainc.com",
                    "url": "https://www.datainc.com/jobs/456",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["New York, NY"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "No",
                    "active": True,
                    "is_visible": True,
                },
            ]
        else:
            listings = util.getDataFromJSON("listings.json")

        util.sortListings(listings)
        today = datetime.now()
        yesterday_midnight = datetime(today.year, today.month, today.day)
        listings = util.filterSummer(listings, "2025", earliest_date=int(yesterday_midnight.timestamp()))

        if not listings:
            print("No listings to post.")
            return

        # Prepare embeds
        embeds = []
        for listing in listings:
            embed = self.create_embed(listing)
            embeds.append(embed)

        # Post embeds in batches of 10
        forum_channel_id = int(os.getenv("FORUM_CHANNEL_ID"))
        forum_channel = self.bot.get_channel(forum_channel_id)

        if not forum_channel:
            print(f"Forum channel with ID {forum_channel_id} not found or inaccessible.")
            return

        thread_title = today.strftime("%A, %B %d, %Y")
        try:
            thread_with_message = await forum_channel.create_thread(
                name=thread_title,
                content=f"Job listings for {thread_title}:"
            )
            thread = thread_with_message.thread
            print(f"Thread created: {thread.jump_url}")

            for i in range(0, len(embeds), 10):
                embed_batch = embeds[i:i + 10]
                await thread.send(embeds=embed_batch)
                print(f"Sent {len(embed_batch)} embeds in a batch.")

        except Exception as e:
            print(f"Error creating thread or posting messages: {e}")

        if TEST_MODE:
            self.posted_today = True

    def create_embed(self, listing):
        """Create a Discord Embed object for a job listing."""
        embed = discord.Embed(
            title=listing["title"],
            url=listing["url"],
            description=f"Posted by **{listing['company_name']}**",
            color=discord.Color.blue(),
            timestamp=datetime.fromtimestamp(listing["date_updated"])
        )
        embed.add_field(name="Locations", value=", ".join(listing["locations"]), inline=False)
        embed.add_field(name="Terms", value=", ".join(listing["terms"]), inline=False)
        embed.add_field(name="Sponsorship", value=listing["sponsorship"], inline=True)
        embed.add_field(name="Active", value="✅" if listing["active"] else "❌", inline=True)

        if listing["company_url"]:
            embed.set_author(name=listing["company_name"], url=listing["company_url"])

        embed.set_footer(text="Last updated")
        return embed

    @post_listings.before_loop
    async def before_post_listings(self):
        print("Waiting until bot is ready...")
        await self.bot.wait_until_ready()
        print("Bot is ready! Starting post_listings loop.")


async def setup(bot):
    """Sets up the PostListings cog."""
    await bot.add_cog(PostListings(bot))
