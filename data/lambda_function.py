import requests
import boto3


def lambda_handler(event, context):
    # Get job listings from SimplifyJobs repo
    GITHUB_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/refs/heads/dev/.github/scripts/listings.json"
    r = requests.get(GITHUB_URL)

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
