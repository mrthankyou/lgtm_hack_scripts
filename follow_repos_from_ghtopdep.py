# python3 follow_repos_from_ghtopdep.py <PATH_TO_GHTOPDEP>

from typing import List
from lgtm import LGTMSite, LGTMDataFilters, LGTMRequestException
from github import Github, GithubException

import os
import sys
import json
import time
import utils.github_api

def save_project_to_lgtm(site: 'LGTMSite', repo_name: str) -> dict:
    print("About to save: " + repo_name)
    # Another throttle. Considering we are sending a request to Github
    # owned properties twice in a small time-frame, I would prefer for
    # this to be here.
    time.sleep(1)

    repo_url: str = 'https://github.com/' + repo_name

    try:
        project = site.follow_repository(repo_url)
    except LGTMRequestException:
        print('issue following repo. skipping for now.')
    except GithubException:
        print('issue following repo. skipping for now.')

    print("Saved the project: " + repo_name)
    return project

site = LGTMSite.create_from_file()
github = utils.github_api.create()
project_keys = []
formatted_data: dict

ghtopdep_file_path = sys.argv[1]

with open(ghtopdep_file_path) as ghtopdep_output_file:
   raw_data = ghtopdep_output_file.read()
   formatted_data = json.loads(raw_data)


for repo_name in formatted_data:
    time.sleep(1)
    try:
        repo = github.get_repo(repo_name)
    except LGTMRequestException:
        print('issue finding repo. skipping for now.')
        continue
    except GithubException:
        print('issue finding repo. skipping for now.')
        continue

    if repo.archived or repo.fork:
        continue

    save_project_to_lgtm(site, repo_name)
