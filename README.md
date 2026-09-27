# Overview
This is an ETL Pipeline. What my somewhat simple code does is it extracts issues and pull requests updated/created after the script last ran (Fallback is at the very start of repo creation), flattens it into readable columns of important data like: dates, information and labels then exports it as a columnar-based parquet file and into a permanent database of all times it has ran.
The parquet files will be used for data analysis.

## Setup
To set up this repo correctly, follow these steps:
- In the repo, create and activate a virtual environment so you can run some scripts in it. To create a venv run these commands in the following order:
    1. cd Drive:/Users/User/PathToProjectFolder
    2. python -m venv .venv
    3. .venv/Scripts/activate
    4. pip install -r requirements.txt
- In the .env.example file in the repo, please add your personal access token. Example: GITHUB_TOKEN=MySecretToken and rename the file to .env
- To see how to create a PAT, [click here](https://www.youtube.com/watch?v=0C-B6bFuQYU)
- In main.py, assign these variables to your liking:
    * owner (the person who owns the target repo)
    * repo (the target repo name)
    * username (Your GitHub Username)
- Run main.py to finish and use the script
- What happens is it extracts your data, flattens it into relevant data, then loads it into a permanent database of every record and a new parquet file (this creates a new file each time so it can see the most recent snapshot of data)
- After this runs, run dashboard.py (optional) to see the dashboard of analytics
- These analytics includes KPI cards and graphs of:
    * Total Issues recorded
    * Amount of different users who have contributed
    * Amount of Stale Items (> 14 days of inactivity)
    * Closed to Open ration Pie Chart
    * Amount of entities (issues/PRs) an author has made
    * A bar chart of amount of each label
    * A Histogram of lead time days to see how long it takes to close an issue
    * Total Issue/PR over time (Records per snapshot)

### Warning
IF you use this, please make sure you have everything correctly set up (every single file in the repo) and DO NOT TOUCH THEM OR IT BREAKS THE SCRIPT (Esepcially timestamp.txt and data.db)

## Next plans
- **Multi Repo:** Currently, this only works on one repo but I plan on making a separate repo to make this work on many repos, this will be at the very end however!
