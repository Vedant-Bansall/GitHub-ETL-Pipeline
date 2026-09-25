# Imports
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

# Access the data
issue_list, pr_list = extract_data(pat_key, owner, repo, username, target_date_str, target_dt)

# Transformed Issues Data, flattened and filtered out, easier readability and better for analysis
transformed_issues = []

## Dictionary Flattening
# Check issues and filter it
for issue in issue_list:
    # Create Fallback Variables
    author = "Ghost"
    closed_by_user = None
    thumbs_up = 0

    # Extractions
    # Author
    if issue.get("user") is not None:
        author = issue["user"]["login"]

    # Closed By User
    if issue.get("closed_by") is not None:
        closed_by_user = issue["closed_by"]["login"]

    # Thumbs Up
    if issue.get("reactions") is not None:
        thumbs_up = issue["reactions"].get("+1", 0)

    # Create filtered issue
    transformed_issues.append({"id": issue.get("id"),
                             "number": issue.get("number"),
                             "title": issue.get("title"),
                             "author": author,
                             "closed_by": closed_by_user,
                             "thumbs_up": thumbs_up,
                             "state": issue.get("state"),
                             "body": issue.get("body"),
                             "created_at": issue.get("created_at"),
                             "closed_at": issue.get("closed_at"),
                             "updated_at": issue.get("updated_at"),
                             "entity_type": "issue"})

# Transformed Pull Requests Data, flattened and filtered out, easier readability and better for analysis
transformed_prs = []

# Check PRs and Filter it
for pr in pr_list:
    # Create Fallback Variables
    author = "Ghost"
    closed_by_user = None
    thumbs_up = 0
    head_branch = None
    base_branch = None

    # Extractions
    # Author
    if pr.get("user") is not None:
        author = pr["user"]["login"]

    # Closed By User
    if pr.get("closed_by") is not None:
        closed_by_user = pr["closed_by"]["login"]

    # Thumbs Up
    if pr.get("reactions") is not None:
        thumbs_up = pr["reactions"].get("+1", 0)

    # Head Branch
    if pr.get("head") is not None:
        head_branch = pr["head"]["ref"]

    # Base Branch
    if pr.get("base") is not None:
        base_branch = pr["base"]["ref"]

    transformed_prs.append({"id": pr.get("id"),
                             "number": pr.get("number"),
                             "title": pr.get("title"),
                             "author": author,
                             "closed_by": closed_by_user,
                             "thumbs_up": thumbs_up,
                             "state": pr.get("state"),
                             "body": pr.get("body"),
                             "created_at": pr.get("created_at"),
                             "closed_at": pr.get("closed_at"),
                             "updated_at": pr.get("updated_at"),
                             "merged_at": pr.get("merged_at"),
                             "draft": pr.get("draft"),
                             "head_branch": head_branch,
                             "base_branch": base_branch,
                             "entity_type": "Pull Request"})