import requests
import boto3


def lambda_handler(event, context):
    # Get job listings from SimplifyJobs repo
    GITHUB_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/refs/heads/dev/.github/scripts/listings.json"
    r = requests.get(GITHUB_URL)
    file_content = r.content

    # Interact with S3 bucket
    s3 = boto3.client("s3")
    bucket_name = "acm-github-data"
    
    # Update existing data to yesterday's data
    curr_file_name = "listings.json"
    prev_file_name = "listings-prev.json"
    s3.copy_object(Bucket=bucket_name, CopySource=f"{bucket_name}/{curr_file_name}", Key=prev_file_name)

    # Put request's data as current data
    s3.put_object(Body=file_content, Bucket=bucket_name, Key=curr_file_name)

    return {
        "statusCode": 200,
        "body": "Job listings uploaded successfully."
    }
