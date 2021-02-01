# This script will look for repos given a search term and language.
from typing import List
from github import Github
from lgtm import LGTMSite
from datetime import datetime

import sys
import yaml
import time

gh_counter = 0
lgtm_counter = 0

# TODO: RUN THIS

# python3 follow_repos_by_search_term.py <LANGUAGE> <SEARCH_TERM>
# Do some basic checks before we run the script

if len(sys.argv) < 3:
    print("Please make sure you provided a language and search term")
    exit

def create_github() -> Github:
    with open("config.yml") as config_file:
        config = yaml.safe_load(config_file)
        github: dict = config['github']
        return Github(github['api_key'])

def current_year() -> int:
    now = datetime.now()
    return now.year

def generate_dates() -> List[str]:
    date_ranges: List[str] = []

    # Github started in 2008
    year_range = list(range(2008, current_year() + 1))

    for i, year in enumerate(year_range):
        date_ranges.append(f'{year}-01-01..{year + 1}-01-01')

    return date_ranges

def find_and_save_projects_to_lgtm(language: str, search_term: str):
    github = create_github()
    site = LGTMSite.create_from_file()

    for date_range in generate_dates():
        repos = github.search_repositories(query=f'language:{language} created:{date_range} {search_term}')
        for repo in repos:
            # Github has rate limiting in place hence why we add a sleep here. More info can be found here:
            # https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
            time.sleep(1)

            global gh_counter
            gh_counter += 1
            print("gh_counter at ", gh_counter)

            if repo.archived or repo.fork:
                continue
            repo_name = repo.full_name
            print("About to save: " + repo_name)
            repo_url: str = 'https://github.com/' + repo_name

            global lgtm_counter
            lgtm_counter += 1
            print("lgtm_counter at ", lgtm_counter)
            time.sleep(1)

            follow_repo_result = site.follow_repository(repo_url)
            print("Saved the project: " + repo_name)

language = sys.argv[1].capitalize()
search_term = sys.argv[2]

print(f'Following repos for the {language} language using the \'{search_term}\' search term.')
find_and_save_projects_to_lgtm(language, search_term)
