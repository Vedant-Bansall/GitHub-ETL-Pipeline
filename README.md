# Overview
This is an ETL Pipeline. What my somewhat simple code does is it extracts issues and pull requests updated/created after the script last ran (Fallback is at the very start of repo creation), flattens it into readable columns of important data like: dates, information and labels then exports it as a columnar-based parquet file and into a permanent database of all times it has ran.
The parquet files will be used for data analysis.

## Setup
To set up this repo correctly, follow these steps:
- In the repo, create and activate a virtual environment so you can run some scripts in it. Once activated, please run pip install -r requirements.txt
- In the .env file in the repo, please add your personal access token. Example: GITHUB_TOKEN=MySecretToken
- In main.py, assign these variables to your liking:
    * owner (the person who owns the target repo)
    * repo (the target repo name)
    * username (Your GitHub Username)
- Run main.py to finish and use the script

### Warning
IF you use this, please make sure you have everything correctly set up (every single file in the repo) and DO NOT TOUCH THEM (Esepcially timestamp.txt and data.db)

## Next plans
- **Tag adder:** Adds relevant tags to specific issues and an slack channel bot to tell you what happens every time it is ran
- **Web App:** Streamlit/Dash Dashboard of Interactive charts and graphs with a few leaderboards (WIP Currently)
- **DuckDB Analysis:** Runs fast SQL Queries on .parquet files to run historical queries without effecting the actual database itself (WIP Currently)
- **Docking Containment:** This will be on a docker container so it can be run on any system
- **AI Summary:** An AI will make a 2 sentence summary of the title and body of the issues/PRs and create a suggested team assignement
- **Multi Repo:** Currently, this only works on one repo but I plan on making a separate repo to make this work on many repos, this will be at the very end however!
