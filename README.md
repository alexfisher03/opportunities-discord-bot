- **Overview**
    - ACM Connect is a Discord bot that takes active internship opportunity listings and posts them daily in any Discord server. Users can invite the bot to their server, and it will create a forum in which it will log internship listings from Simplify's Summer Internship repository. New listings are posted once daily, at 12:00:00 UTC. 
    - ACM Connect uses an AWS S3 bucket to store Simplify listings and an AWS lambda function to retrieve new listings from Simplify as soon as they are posted. Once daily, at 00:00:00 EST, the lambda function scrapes the new simplify listings for its respective day, formats them, and sends them to the S3 bucket. The bot scripts will then post all new listings for the current day at 12:00:00 UTC.

Tech Stack:
  - AWS
    - UC2 Instance
    - S3 Bucket
    - Lambda Function
  - Python
    - Discord.py

- Acknowledgements
    - Developed by Alex Fisher, Jason Tenczar, Steve Sajeev, Jacob Frankel, and Alex Milanes
