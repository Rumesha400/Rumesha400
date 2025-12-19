import requests
import os
from datetime import datetime
import pytz

USERNAME = "Rumesha400"
TOKEN = os.environ["GH_TOKEN"]

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

user_data = requests.get(
    f"https://api.github.com/users/{USERNAME}",
    headers=HEADERS
).json()

repos = requests.get(
    "https://api.github.com/user/repos?per_page=100",
    headers=HEADERS
).json()

public_repos = user_data.get("public_repos", 0)
private_repos = sum(1 for r in repos if r.get("private"))

total_commits = 0
total_prs = 0

for repo in repos:
    owner = repo["owner"]["login"]
    name = repo["name"]

    commits = requests.get(
        f"https://api.github.com/repos/{owner}/{name}/commits?author={USERNAME}",
        headers=HEADERS
    ).json()

    pulls = requests.get(
        f"https://api.github.com/repos/{owner}/{name}/pulls?state=all",
        headers=HEADERS
    ).json()

    if isinstance(commits, list):
        total_commits += len(commits)
    if isinstance(pulls, list):
        total_prs += len(pulls)

ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist).strftime("%Y-%m-%d %H:%M IST")

stats_block = f"""
### 📊 Complete GitHub Statistics (Including Private Repos)
- **Total Pull Requests**: **{total_prs}**
- **Public Repositories**: **{public_repos}**
- **Private Repositories**: **{private_repos}**
- **Total Commits**: **{total_commits}**
- **Last Updated**: **{now}**
"""

with open("README.md", "r") as f:
    content = f.read()

start = "<!--START_GH_STATS-->"
end = "<!--END_GH_STATS-->"

new_content = content.split(start)[0] + start + stats_block + end + content.split(end)[1]

with open("README.md", "w") as f:
    f.write(new_content)
