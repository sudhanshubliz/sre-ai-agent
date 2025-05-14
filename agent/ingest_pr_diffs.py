import requests

def fetch_pr_diff(repo_owner, repo_name, pr_number, token):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3.diff"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(f"data/diffs/pr_{pr_number}.diff", "w") as f:
            f.write(response.text)
        print(f"Downloaded diff for PR #{pr_number}")
    else:
        print("Failed to fetch diff", response.status_code)