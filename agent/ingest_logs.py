# -------------------------
# agent/ingest_logs.py
# -------------------------
import requests
import os

def fetch_github_actions_logs(repo_owner, repo_name, run_id, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs/{run_id}/logs"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(f"data/logs/{run_id}.zip", "wb") as f:
            f.write(response.content)
        print(f"Downloaded logs for run {run_id}")
    else:
        print("Failed to fetch logs", response.status_code)