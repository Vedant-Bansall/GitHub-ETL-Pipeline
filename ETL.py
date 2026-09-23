import os

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
query_paramaters = {"since": "2024-01-01T00:00:00Z", "state": "all", "per_page": 100}

# Create Response
response = requests.get(url, headers=headers, params=query_paramaters)
r_json = response.json()

# Find Rate Limit stuff
limit = response.headers.get("X-RateLimit-Limit")
remaining = response.headers.get("X-RateLimit-Remaining")
reset_time = response.headers.get("X-RateLimit-Reset")
used = response.headers.get("X-RateLimit-Used")

print(f"Rate Limit: {remaining}/{limit} remaining (Used: {used})")
print(f"Resets at (epoch timestamp): {reset_time}")