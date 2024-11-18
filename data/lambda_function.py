import requests
import boto3

import os
from dotenv import load_dotenv
load_dotenv()

GH_API_TOKEN = os.getenv("GH_API_TOKEN")
ENDPOINT = os.getenv("ENDPOINT")


def lambda_handler(event, context):
    # Get job listings from SimplifyJobs repo
    headers = {
        "Accept": "application/vnd.github.raw+json",
        "Authorization": f"Bearer {GH_API_TOKEN}"
    }

    r = requests.get(ENDPOINT, headers=headers)

    # Upload file to S3 bucket
    bucket_name = "acm-github-data"
    file_name = "listings.json"
    file_content = r.content

    s3 = boto3.client("s3")
    s3.put_object(Body=file_content, Bucket=bucket_name, Key=file_name)

    return {
        "statusCode": 200,
        "body": "Job listings uploaded successfully."
    }
