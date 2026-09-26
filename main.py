import os  # noqa: I001
from datetime import datetime

from dotenv import load_dotenv

from extract import extract_data
from transform import transform_data
from load import load_data

# Load values
load_dotenv()

# Get params, Not permanent
pat_key = os.getenv("GITHUB_TOKEN")
owner = "pallets"
repo = "flask"
username = "Vedant-Bansall"
target_date_str = "2026-09-01T00:00:00Z"
target_dt = datetime.fromisoformat(target_date_str.replace("Z", "+00:00"))

standard_issues, pull_requests = extract_data(pat_key, owner, repo, username, target_date_str, target_dt)
transformed_dataset = transform_data(standard_issues, pull_requests)
print(load_data(transformed_dataset))