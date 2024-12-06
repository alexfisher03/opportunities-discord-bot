# ACM Connect - Opportunities and Events Discord Bot
![ConnectBanner](https://github.com/user-attachments/assets/9f99f591-6c65-4666-8b93-4c2f55da2d1e)

<img width="616" alt="image" src="https://github.com/user-attachments/assets/7751b58e-99bd-4e2c-a9e6-80c93e2f2192">

**Overview**
    - ACM Connect is a Discord bot that takes active internship opportunity listings and posts them daily in any Discord server. Users can invite the bot to their server, and it will create a forum in which it will log internship listings from Simplify's Summer Internship repository. New listings are posted once daily, at 12:00:00 UTC. 
    - ACM Connect uses an AWS S3 bucket to store Simplify listings and an AWS lambda function to retrieve new listings from Simplify as soon as they are posted. Once daily, at 9:00PM EST, the lambda function scrapes the new simplify listings for its respective day, formats them, and sends them to the S3 bucket. The bot scripts will then post all new listings for the current day at 9:15EST.
 
**Tech Stack**
  - AWS
    - EC2 Instance
    - S3 Bucket
    - Lambda Function
  - Python
    - Discord.py

**Acknowledgements**
    - Developed by Alex Fisher, Jason Tenczar, Steve Sajeev, Jacob Frankel, and Alex Milanes
