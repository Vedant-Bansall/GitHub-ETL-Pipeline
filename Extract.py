# Imports
from datetime import datetime, timezone

import requests


# Custom Errors
class ExtractionError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class LimitError(ExtractionError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ServerIssueError(ExtractionError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

### Extract
def extract_data(key: str, owner: str, repo: str, username: str, target_date_str: str, target_dt: datetime) -> tuple[list, list]:
    ## Issues
    # Create Response params
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {key}", "User-Agent": username}
    query_paramaters = {"since": target_date_str, "state": "all", "per_page": 100}

    # List of all
    master_list = []

    # Pagination Loop 1 - Std Issues
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
                    raise LimitError("You have no more requests remaining")
                else:
                    print(f"Rate Limit: {remaining}/{limit} remaining (Used: {used})")
                    print(f"Resets at (epoch timestamp): {reset_readable}")
            else:
                raise ExtractionError("You have no more requests remaining or a serverside error happened")

        # Raise Errors:
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "Unknown"
            if status in [403, 429]:
                raise LimitError(f"Rate Limit Exceeded or access forbidden: {status}")

            else:
                raise ServerIssueError(f"HTTP Error Occured: {status}")

        except requests.exceptions.RequestException:
            raise ServerIssueError("Serverside Error")

        query_paramaters = None # Reset params

        master_list.extend(response_json) # Add to all

        link = response.headers.get("Link")

        # Link parsing
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

    standard_issues = [item for item in master_list if item.get("pull_request") is None]

    ## Pull Requests
    # New response params
    pull_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    pull_query_paramaters = {"state": "all", "per_page": 100, "sort": "updated", "direction": "desc"}

    pull_list = []

    # Pagination Loop 2 - Pull Requests
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
                    raise LimitError("You have no more requests remaining")
                else:
                    print(f"Rate Limit: {remaining}/{limit} remaining (Used: {used})")
                    print(f"Resets at (epoch timestamp): {reset_readable}")
            else:
                raise ExtractionError("You have no more requests remaining or a serverside error happened")

        # Raise Errors
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "Unknown"
            if status in [403, 429]:
                raise LimitError(f"Rate Limit Exceeded or access forbidden: {status}")

            else:
                raise ServerIssueError(f"HTTP Error Occured: {status}")

        except requests.exceptions.RequestException:
            raise ServerIssueError("Serverside Error")

        pull_query_paramaters = None # Reset Params

        # Get items from only AFTER the most recent occurence of script running
        for item in pull_response_json:
            raw_updated_at = item["updated_at"]
            item_dt = datetime.fromisoformat(raw_updated_at.replace("Z", "+00:00"))
            if item_dt >= target_dt:
                pull_list.append(item)
            else:
                pull_url = None
                break

        if pull_url != None:
            pull_link = pull_response.headers.get("Link")

            # Parsing
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

    # Seperate items
    if not master_list:
        raise ExtractionError("Extraction completed, but 0 issues/PRs matched the filter criteria.")

    return standard_issues, pull_list # Returns items to be used