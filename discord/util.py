"""
See
    https://github.com/SimplifyJobs/Summer2025-Internships/blob/dev/.github/README-scripts.md
    Based on https://github.com/SimplifyJobs/Summer2025-Internships/blob/dev/.github/scripts/util.py
"""
import json
from datetime import datetime


# TODO: instead of getting data from JSON, get from S3 bucket
# NOTE: Need to have json files in same directory
def getDataFromJSON(filename):
    with open(filename) as f:
        listings = json.load(f)
        return listings

# TODO: instead of saving data to JSON, save to S3 bucket
# NOTE: Creates json file in same directory
def saveDataToJSON(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def sortListings(listings):
    oldestListingFromCompany = {}
    linkForCompany = {}

    for listing in listings:
        date_posted = listing["date_posted"]
        if listing["company_name"].lower() not in oldestListingFromCompany or oldestListingFromCompany[listing["company_name"].lower()] > date_posted:
            oldestListingFromCompany[listing["company_name"].lower(
            )] = date_posted
        if listing["company_name"] not in linkForCompany or len(listing["company_url"]) > 0:
            linkForCompany[listing["company_name"]] = listing["company_url"]

    listings.sort(
        key=lambda x: (
            x["active"],  # Active listings first
            datetime(
                datetime.fromtimestamp(x["date_posted"]).year,
                datetime.fromtimestamp(x["date_posted"]).month,
                datetime.fromtimestamp(x["date_posted"]).day
            ),
            x['company_name'].lower(),
            x['date_updated']
        ),
        reverse=True
    )

    for listing in listings:
        listing["company_url"] = linkForCompany[listing["company_name"]]

    return listings


def filterSummer(listings, year, earliest_date):
    return [listing for listing in listings if listing["is_visible"] and any(f"Summer {year}" in item for item in listing["terms"]) and listing['date_posted'] > earliest_date]
