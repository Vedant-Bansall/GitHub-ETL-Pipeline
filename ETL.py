import os
from datetime import datetime, timezone
from sys import exit

import requests
from dotenv import load_dotenv

### Extract
# Load values
load_dotenv()

# Get create variables
pat_key = os.getenv("GITHUB_TOKEN")
owner = "pallets"
repo = "flask"
username = "Vedant-Bansall"
target_date_str = "2026-09-01T00:00:00Z"
target_dt = datetime.fromisoformat(target_date_str.replace("Z", "+00:00"))

## Issues
# Create Response params
url = f"https://api.github.com/repos/{owner}/{repo}/issues"
headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {pat_key}", "User-Agent": username}
query_paramaters = {"since": target_date_str, "state": "all", "per_page": 100}

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

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "Unknown"
        if status in [403, 429]:
            print("Rate Limit Exceeded or access forbidden")
            exit()

        else:
            print(f"HTTP Error Occured: {status}")
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

standard_issues = [item for item in master_list if item.get("pull_request") is None]

## Pull Requests
pull_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
pull_query_paramaters = {"state": "all", "per_page": 100, "sort": "created", "direction": "desc"}

pull_list = []

while pull_url != None:
    try:
        # Create Response
        pull_response = requests.get(pull_url, headers=headers, params=pull_query_paramaters)

        # Rest of response stuff
        pull_response.raise_for_status()
        pull_response_json = pull_response.json()

        # Find Rate Limits and others
        limit = pull_response.headers.get("X-RateLimit-Limit")
        remaining = pull_response.headers.get("X-RateLimit-Remaining")
        reset_time = pull_response.headers.get("X-RateLimit-Reset")
        used = pull_response.headers.get("X-RateLimit-Used")

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

    except requests.exceptions.HTTPError as e:
        status = e.response.status_code if e.response is not None else "Unknown"
        if status in [403, 429]:
            print("Rate Limit Exceeded or access forbidden")
            exit()

        else:
            print(f"HTTP Error Occured: {status}")
            exit()

    except requests.exceptions.RequestException:
        print("Serverside Error")
        exit()

    pull_query_paramaters = None

    for item in pull_response_json:
        raw_created_at = item["created_at"]
        item_dt = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
        if item_dt >= target_dt:
            pull_list.append(item)
        else:
            pull_url = None
            break

    if pull_url != None:
        pull_link = pull_response.headers.get("Link")

        if pull_link != None:
            pull_link_parsed = requests.utils.parse_header_links(str(pull_link))
            pull_link_found = None
            for i in range(len(pull_link_parsed)):
                if pull_link_parsed[i]["rel"] == "next":
                    pull_url = pull_link_parsed[i]["url"]
                    pull_link_found = pull_url
                    break
            pull_url = pull_link_found

        else:
            pull_url = None

    else:
        pull_url = None