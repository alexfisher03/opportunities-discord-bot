# ACM Connect - Opportunities and Events Discord Bot
![ConnectBanner](https://github.com/user-attachments/assets/9f99f591-6c65-4666-8b93-4c2f55da2d1e)

<img width="616" alt="image" src="https://github.com/user-attachments/assets/7751b58e-99bd-4e2c-a9e6-80c93e2f2192">

## 🚀 **Features**

### 🤖 Daily Internship Postings  
- Automatically posts **active internship opportunities** from Simplify's Summer Internship repository.  
- Posts occur **once daily** at **9:15 PM EST** in a dedicated forum created by the bot.

### 🌐 Easy Server Integration  
- Users can invite ACM Connect to their Discord servers.  
- Bot automatically sets up a forum for internship postings.

### 🔄 Automated Updates  
- Uses AWS Lambda to **scrape and retrieve listings** from Simplify every day at **9:00 PM EST**.  
- Newly scraped listings are **formatted and stored** in an AWS S3 bucket.  
- Bot retrieves and posts the **current day's listings** from the S3 bucket.

---

## 🛠️ **Tech Stack**

- **AWS**: For serverless data processing and storage  
  - **Lambda**: Scrapes Simplify internship listings daily.  
  - **S3 Bucket**: Stores and organizes daily internship data.  
  - **EC2 Instance**: Hosts the Discord bot scripts.
- **Python**: Core programming language for bot functionality.  
- **Discord.py**: Framework for seamless Discord integration.

---

## 👥 **Acknowledgements**  

ACM Connect was proudly developed by:  
- Alex Fisher  
- Jason Tenczar  
- Steve Sajeev  
- Jacob Frankel  
- Alex Milanes  

---

### 📝 **How to Get Started**
(Bot is exclusive for the UF ACM discord server as of now)

---

We hope ACM Connect enhances your journey to finding the perfect internship. For questions or issues, feel free to open an issue on this repository or reach out to the development team.

Happy job hunting! 🚀
