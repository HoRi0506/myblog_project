import requests
from datetime import datetime

GITHUB_API_URL = 'https://api.github.com/users/{username}/repos'

def update_repositories():
    try:
        # GitHub API 호출
        response = requests.get(GITHUB_API_URL.format(username='HoRi0506'))  # 본인의 GitHub username
        repos = response.json()

        # repository 정보 업데이트 로직 (여기서 로컬 DB에 저장하거나 필요에 따라 처리)
        for repo in repos:
            created_at = datetime.strptime(repo['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            pushed_at = datetime.strptime(repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ")
            # repository 데이터를 DB에 저장하는 로직 추가
            print(f"Repository: {repo['name']} updated successfully.")

    except Exception as e:
        print(f"Error updating repositories: {str(e)}")