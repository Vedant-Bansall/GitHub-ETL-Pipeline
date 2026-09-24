import os
from datetime import datetime

from dotenv import load_dotenv

from Extract import extract_data

# Load values
load_dotenv()

# Get params
pat_key = os.getenv("GITHUB_TOKEN")
owner = "pallets"
repo = "flask"
username = "Vedant-Bansall"
target_date_str = "2026-09-01T00:00:00Z"
target_dt = datetime.fromisoformat(target_date_str.replace("Z", "+00:00"))

issue_list, pr_list = extract_data(pat_key, owner, repo, username, target_date_str, target_dt)