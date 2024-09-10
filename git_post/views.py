import requests
from datetime import datetime, timedelta
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils.timezone import now, make_aware
import pytz
from django.conf import settings
import json, os

# GitHub API URL (본인의 GitHub username으로 변경)
GITHUB_API_URL = 'https://api.github.com/users/{username}/repos'
NEW_REPOSITORY_DAYS = 15  # New 레이블 표시 기간

token_file_path = os.path.join(settings.BASE_DIR, 'token.json')

try:
    # token.json 파일 읽기
    with open(token_file_path) as tk:
        json_data = json.load(tk)
        GITHUB_TOKEN = json_data['token']  # Personal Access Token
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading GitHub token: {str(e)}")
    GITHUB_TOKEN = None  # 토큰을 찾지 못한 경우 None으로 설정

def git_post(request):
    try:
        if not GITHUB_TOKEN:
            raise Exception("GitHub token is missing or invalid")

        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',  # 인증 토큰을 헤더에 포함
        }

        # GitHub API 호출 (GitHub 계정의 repository 목록 가져오기)
        response = requests.get(GITHUB_API_URL.format(username='HoRi0506'), headers=headers)

        # API 응답 상태 코드 확인
        if response.status_code == 403:
            raise Exception(f"GitHub API error: {response.status_code} - Rate Limit Exceeded. Try again later or use an authenticated request.")
        elif response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code}")

        repos = response.json()

        # 응답이 리스트인지 확인
        if not isinstance(repos, list):
            raise Exception("GitHub API response is not a list")

        # 'New'와 'Update' 여부 추가
        for repo in repos:
            # GitHub에서 받은 datetime을 UTC 기반으로 timezone-aware로 변환
            created_at = make_aware(datetime.strptime(repo['created_at'], "%Y-%m-%dT%H:%M:%SZ"), pytz.UTC)
            pushed_at = make_aware(datetime.strptime(repo['pushed_at'], "%Y-%m-%dT%H:%M:%SZ"), pytz.UTC)

            # 상태 필드를 리스트로 저장 (New와 Update 동시에 가질 수 있음)
            repo['status'] = []
            if (now() - timedelta(days=NEW_REPOSITORY_DAYS)) < created_at:
                repo['status'].append('New')
            if (now() - timedelta(days=NEW_REPOSITORY_DAYS)) < pushed_at:
                repo['status'].append('Update')

            # 사용 언어 정보 추가
            languages_url = repo.get('languages_url', '')
            if languages_url:
                lang_response = requests.get(languages_url, headers=headers)
                repo['languages'] = ', '.join(lang_response.json().keys()) if lang_response.status_code == 200 else 'Unknown'
            else:
                repo['languages'] = 'Unknown'

        # 'New'와 'Update' 여부에 따라 정렬
        def sort_key(repo):
            status_priority = 0
            if 'New' in repo['status'] and 'Update' in repo['status']:
                status_priority = 3  # New + Update 모두 있으면 가장 높은 우선순위
            elif 'New' in repo['status']:
                status_priority = 2  # New만 있으면 그 다음
            elif 'Update' in repo['status']:
                status_priority = 1  # Update만 있으면 그 다음
            else:
                status_priority = 0  # 아무 상태도 없으면 우선순위 낮음
            return (status_priority, repo['pushed_at'] if 'pushed_at' in repo else repo['created_at'])


        # 상태 및 pushed_at을 기준으로 정렬
        repos = sorted(repos, key=sort_key, reverse=True)

        # Pagination 처리 (한 페이지당 9개의 repository 표시)
        paginator = Paginator(repos, 9)  # 9개의 아이템을 한 페이지로
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'git_post/repository_list.html', 
                      {'page_obj': page_obj,
                       'MEDIA_URL': settings.MEDIA_URL  # MEDIA_URL을 템플릿에 전달
                       })
    except Exception as e:
        print(f"Error fetching repositories: {str(e)}")
        return render(request, 'git_post/repository_list.html', {'page_obj': []})
