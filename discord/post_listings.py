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
                    "title": "Frontend Developer Intern",
                    "company_name": "TechWave",
                    "company_url": "https://www.techwave.com",
                    "url": "https://www.techwave.com/jobs/frontend-dev",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Austin, TX", "Remote"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "Yes",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Backend Developer Intern",
                    "company_name": "CodeLabs",
                    "company_url": "https://www.codelabs.com",
                    "url": "https://www.codelabs.com/jobs/backend-dev",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Seattle, WA", "Remote"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "No",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Machine Learning Intern",
                    "company_name": "DataMind",
                    "company_url": "https://www.datamind.com",
                    "url": "https://www.datamind.com/jobs/ml-intern",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["New York, NY"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "Yes",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Game Developer Intern",
                    "company_name": "PixelWorks",
                    "company_url": "https://www.pixelworks.com",
                    "url": "https://www.pixelworks.com/jobs/game-dev",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Los Angeles, CA"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "No",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Full Stack Engineer Intern",
                    "company_name": "InnovateX",
                    "company_url": "https://www.innovatex.com",
                    "url": "https://www.innovatex.com/jobs/fullstack-intern",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["San Francisco, CA"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "Yes",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Cloud Computing Intern",
                    "company_name": "Cloudify",
                    "company_url": "https://www.cloudify.com",
                    "url": "https://www.cloudify.com/jobs/cloud-intern",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Remote"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "No",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Cybersecurity Intern",
                    "company_name": "SecureTech",
                    "company_url": "https://www.securetech.com",
                    "url": "https://www.securetech.com/jobs/cyber-intern",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Boston, MA"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "Yes",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Mobile App Developer Intern",
                    "company_name": "Appify",
                    "company_url": "https://www.appify.com",
                    "url": "https://www.appify.com/jobs/mobile-dev",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Remote", "Chicago, IL"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "No",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Data Analyst Intern",
                    "company_name": "DataWorks",
                    "company_url": "https://www.dataworks.com",
                    "url": "https://www.dataworks.com/jobs/data-analyst",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Atlanta, GA"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "Yes",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Blockchain Developer Intern",
                    "company_name": "CryptoBuilders",
                    "company_url": "https://www.cryptobuilders.com",
                    "url": "https://www.cryptobuilders.com/jobs/blockchain-dev",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Miami, FL"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "No",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "DevOps Engineer Intern",
                    "company_name": "CloudOps",
                    "company_url": "https://www.cloudops.com",
                    "url": "https://www.cloudops.com/jobs/devops-intern",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Seattle, WA"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "Yes",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "AI Research Intern",
                    "company_name": "BrainAI",
                    "company_url": "https://www.brainai.com",
                    "url": "https://www.brainai.com/jobs/ai-research",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Remote"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "No",
                    "active": True,
                    "is_visible": True,
                },
                {
                    "title": "Quality Assurance Engineer Intern",
                    "company_name": "Testify",
                    "company_url": "https://www.testify.com",
                    "url": "https://www.testify.com/jobs/qa-engineer",
                    "date_posted": datetime.now().timestamp(),
                    "date_updated": datetime.now().timestamp(),
                    "locations": ["Denver, CO"],
                    "terms": ["Summer 2025"],
                    "sponsorship": "Yes",
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

        # Post embeds in batches within the same thread
        forum_channel_id = int(os.getenv("FORUM_CHANNEL_ID"))
        forum_channel = self.bot.get_channel(forum_channel_id)

        if not forum_channel:
            print(f"Forum channel with ID {forum_channel_id} not found or inaccessible.")
            return

        # Determine the thread title based on the season
        thread_title = self.generate_thread_title(today)

        try:
            thread_with_message = await forum_channel.create_thread(
                name=thread_title,
                content=f"Job listings for {thread_title}:"
            )
            thread = thread_with_message.thread  # Extract the thread object
            print(f"Thread created: {thread.jump_url}")

            # Send batches in the same thread
            await self.send_batches_in_thread(thread, embeds)

        except Exception as e:
            print(f"Error creating thread or posting messages: {e}")

        if TEST_MODE:
            self.posted_today = True

    async def send_batches_in_thread(self, thread, embeds):
        """Send embeds in batches within the same thread."""
        MAX_EMBEDS = 10
        MAX_CHARACTERS = 2000
        current_batch = []

        def calculate_batch_size(embed_batch):
            total_size = 0
            for embed in embed_batch:
                total_size += len(embed.title or "") + len(embed.description or "")
                total_size += sum(len(field.name or "") + len(field.value or "") for field in embed.fields)
                total_size += len(embed.footer.text or "") if embed.footer else 0
                return total_size

        for embed in embeds:
            if len(current_batch) >= MAX_EMBEDS or calculate_batch_size(current_batch + [embed]) > MAX_CHARACTERS:
                # Post the current batch in the same thread
                acm_logo = discord.File("acm_logo.png", filename="acm_logo.png")
                await thread.send(embeds=current_batch, files=[acm_logo])
                print(f"Sent {len(current_batch)} embeds in a batch.")
                current_batch = []

            # Add the current embed to the batch
            current_batch.append(embed)

        # Post any remaining embeds
        if current_batch:
            acm_logo = discord.File("acm_logo.png", filename="acm_logo.png")
            await thread.send(embeds=current_batch, files=[acm_logo])
            print(f"Sent {len(current_batch)} embeds in the final batch.")


    def create_embed(self, listing):
        """Create a Discord Embed object for a job listing."""
        # Purple embed color
        embed = discord.Embed(
            title=listing["title"],
            url=listing["url"],
            description=f"Posted by **{listing['company_name']}**",
            color=0x5865f2,
            timestamp=datetime.fromtimestamp(listing["date_updated"])
        )
        # Add fields for job details
        embed.add_field(name="Locations", value=", ".join(listing["locations"]), inline=False)
        embed.add_field(name="Terms", value=", ".join(listing["terms"]), inline=False)
        embed.add_field(name="Sponsorship", value=listing["sponsorship"], inline=True)
        embed.add_field(name="Active", value="✅" if listing["active"] else "❌", inline=True)

        # Set author with company name and URL
        if listing["company_url"]:
            embed.set_author(name=listing["company_name"], url=listing["company_url"])

        # Set footer with logo and last updated timestamp
        acm_logo_path = "acm_logo.png"
        embed.set_footer(
            text=f"Last updated • {datetime.fromtimestamp(listing['date_updated']).strftime('%m/%d/%Y %I:%M %p')}",
            icon_url=f"attachment://{acm_logo_path}"
        )
        return embed


    def generate_thread_title(self, today):
        """Generate a thread title based on the season and date."""
        def get_season(month):
            if 8 <= month <= 12:  # August to December
                return "FALL"
            elif 1 <= month <= 5:  # January to May
                return "SPRING"
            elif 6 <= month <= 7:  # June to July
                return "SUMMER"
            return "UNKNOWN"

        season = get_season(today.month)
        return f"{season} {today.year % 100}: {today.strftime('%B %d')}"

    @post_listings.before_loop
    async def before_post_listings(self):
        print("Waiting until bot is ready...")
        await self.bot.wait_until_ready()
        print("Bot is ready! Starting post_listings loop.")


async def setup(bot):
    """Sets up the PostListings cog."""
    await bot.add_cog(PostListings(bot))
