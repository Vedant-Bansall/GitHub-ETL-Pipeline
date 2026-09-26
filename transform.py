# Imports
from datetime import datetime, timezone


# Transform Data
def transform_data(issue_list: list, pr_list: list) -> list:
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

        # Get datetime objects as variables
        issue_created_dt = datetime.fromisoformat(issue.get("created_at").replace("Z", "+00:00")) if issue.get("created_at") is not None else None
        issue_closed_dt = datetime.fromisoformat(issue.get("closed_at").replace("Z", "+00:00")) if issue.get("closed_at") is not None else None
        issue_updated_dt = datetime.fromisoformat(issue.get("updated_at").replace("Z", "+00:00")) if issue.get("updated_at") is not None else None

        # Time Metrics
        # Lead Time Days (How long it lasted)
        issue_lead_time_days = (issue_closed_dt - issue_created_dt).total_seconds() / 86400 if issue_closed_dt and issue_created_dt else None

        # Stale Flag
        issue_is_stale = (datetime.now(timezone.utc) - issue_updated_dt).days > 15 if issue_updated_dt else False

        # Label Assignment
        issue_labels = [label["name"] for label in issue.get("labels") or []]

        # Create filtered issue
        transformed_issues.append({"id": issue.get("id"),
                                "number": issue.get("number"),
                                "title": issue.get("title"),
                                "author": author,
                                "closed_by": closed_by_user,
                                "thumbs_up": thumbs_up,
                                "state": issue.get("state"),
                                "body": issue.get("body"),
                                "created_at": issue_created_dt,
                                "closed_at": issue_closed_dt,
                                "updated_at": issue_updated_dt,
                                "merged_at": None, # For standardisation
                                "draft": False, # For standardisation
                                "head_branch": None, # For standardisation
                                "base_branch": None, # For standardisation
                                "lead_time_days": issue_lead_time_days,
                                "is_stale": issue_is_stale,
                                "labels": issue_labels,
                                "entity_type": "Issue"})

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

        # Get datetime objects as variables
        pr_created_dt = datetime.fromisoformat(pr.get("created_at").replace("Z", "+00:00")) if pr.get("created_at") is not None else None
        pr_closed_dt = datetime.fromisoformat(pr.get("closed_at").replace("Z", "+00:00")) if pr.get("closed_at") is not None else None
        pr_updated_dt = datetime.fromisoformat(pr.get("updated_at").replace("Z", "+00:00")) if pr.get("updated_at") is not None else None
        pr_merged_dt = datetime.fromisoformat(pr.get("merged_at").replace("Z", "+00:00")) if pr.get("merged_at") is not None else None

        # Time Metrics
        # Lead Time Days (How long it lasted)
        pr_lead_time_days = (pr_closed_dt - pr_created_dt).total_seconds() / 86400 if pr_closed_dt and pr_created_dt else None

        # Stale Flag
        pr_is_stale = (datetime.now(timezone.utc) - pr_updated_dt).days > 14 if pr_updated_dt else False

        # Label Assignment
        pr_labels = [label["name"] for label in pr.get("labels") or []]

        transformed_prs.append({"id": pr.get("id"),
                                "number": pr.get("number"),
                                "title": pr.get("title"),
                                "author": author,
                                "closed_by": closed_by_user,
                                "thumbs_up": thumbs_up,
                                "state": pr.get("state"),
                                "body": pr.get("body"),
                                "created_at": pr_created_dt,
                                "closed_at": pr_closed_dt,
                                "updated_at": pr_updated_dt,
                                "merged_at": pr_merged_dt,
                                "draft": pr.get("draft"),
                                "head_branch": head_branch,
                                "base_branch": base_branch,
                                "lead_time_days": pr_lead_time_days,
                                "is_stale": pr_is_stale,
                                "labels": pr_labels,
                                "entity_type": "PullRequest"})

    transformed_dataset = transformed_prs + transformed_issues
    return transformed_dataset
