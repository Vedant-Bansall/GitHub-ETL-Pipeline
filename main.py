import os  # noqa: I001
from datetime import datetime

from dotenv import load_dotenv

from extract import extract_data
from transform import transform_data
from load import load_data, data_to_parquet

# Load values
load_dotenv()

# Get params, Not permanent
pat_key = os.getenv("GITHUB_TOKEN")
owner = "pallets"
repo = "flask"
username = "Vedant-Bansall"
if os.path.getsize("timestamp.txt") == 0:
    target_date_str = "2008-01-01T00:00:00Z"
else:
    with open("timestamp.txt") as tstxt:
        target_date_str = tstxt.read()
    
target_dt = datetime.fromisoformat(target_date_str.replace("Z", "+00:00"))

standard_issues, pull_requests = extract_data(pat_key, owner, repo, username, target_date_str, target_dt)
if standard_issues or pull_requests:
    transformed_dataset = transform_data(standard_issues, pull_requests)
    load_data(transformed_dataset)
    data_to_parquet(transformed_dataset)
    print(f"Fetched:\n• {len(standard_issues)} Issues\n• {len(pull_requests)} Pull Requests")

else:
    print("Extraction completed, but 0 issues/PRs matched the filter criteria.")