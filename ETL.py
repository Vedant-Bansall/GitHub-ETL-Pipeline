import os
from datetime import datetime, timezone
from sys import exit

import requests
from dotenv import load_dotenv

## Extract
# Load values
load_dotenv()

# Get PAT
pat_key = os.getenv("GITHUB_TOKEN")

# Create Response params
url = "https://api.github.com/repos/pallets/flask/issues"
headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {pat_key}"}
query_paramaters = {"since": "2026-09-01T00:00:00Z", "state": "all", "per_page": 100}

# Create Response
master_list = []

while url != None:
    try:
        # Create Response
        response = requests.get(url, headers=headers, params=query_paramaters)

        # Rest of response stuff
        response.raise_for_status()
        response_json = response.json()

        # Find Rate Limits and others
        limit = response.headers.get("X-RateLimit-Limit")
        remaining = response.headers.get("X-RateLimit-Remaining")
        reset_time = response.headers.get("X-RateLimit-Reset")
        used = response.headers.get("X-RateLimit-Used")

        # Checks remaining
        if remaining != None and reset_time != None:
            reset_readable = datetime.fromtimestamp(int(reset_time), tz=timezone.utc)
            if int(remaining) < 20 and int(remaining) != 0:
                print(f"You do not have many Requests left, you only have {int(remaining)} remaining")
            elif int(remaining) <= 0:
                print("You have no more requests remaining")
                exit()
            else:
                print(f"Rate Limit: {remaining}/{limit} remaining (Used: {used})")
                print(f"Resets at (epoch timestamp): {reset_readable}")
        else:
            print("You have no more requests remaining or a serverside error happened")
            exit()

    except requests.exceptions.HTTPError:
        if response.status_code in [403, 429]:
            print("Rate Limit Exceeded or access forbidden")
            exit()

        else:
            print(f"HTTP Error Occured: {response.status_code}")
            exit()

    except requests.exceptions.RequestException:
        print("Serverside Error")
        exit()

    query_paramaters = None

    master_list.extend(response_json)

    link = response.headers.get("Link")

    if link != None:
        link_parsed = requests.utils.parse_header_links(str(link))
        link_found = None
        for i in range(len(link_parsed)):
            if link_parsed[i]["rel"] == "next":
                url = link_parsed[i]["url"]
                link_found = url
                break
        url = link_found

    else:
        url = None

# Seperate items
if not master_list:
    print("Extraction completed, but 0 issues/PRs matched the filter criteria.")
    exit()

pull_requests = [item for item in master_list if "pull_request" in item]
standard_issues = [item for item in master_list if "pull_request" not in item]