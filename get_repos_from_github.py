# THIS IS A MASTER SCRIPT. IT'S GOAL IS TO MAKE IT EVEN EASIER TO USE THE LGTM HACK SCRIPTS.
# BY JUST RUNNING THIS ONE COMMAND WE CAN RUN ANY SERIES OF COMMANDS WE WANT. 

# python3 get_repos_from_github.py search_term <SEARCH_TERM>          <LANGUAGE> <CUSTOM_LIST_NAME>
# python3 get_repos_from_github.py stars_count <MIN_STARS>            <LANGUAGE> <CUSTOM_LIST_NAME>
# python3 get_repos_from_github.py ghtopdep    <GITHUB_REPO_URL>              <CUSTOM_LIST_NAME>

from typing import List
from lgtm import LGTMSite, LGTMDataFilters

import os
import sys
import json
import time
import numpy
import shutil
import subprocess
import utils.github_api
import utils.github_dates
import utils.cacher

# handles extracting command-line arguments
def get_argument(index):
    try:
        return sys.argv[index]
    except IndexError:
        None

def break_array_into_lists(list: List[str], n: int):
    return [list[i:i + n] for i in range(0, len(list), n)]

def save_repos_to_cached_file(repo_list: List[str], custom_list_name: str):
    flattened_repo_list = [item for sublist in repo_list for item in sublist]
    unique_repo_list = list(set(flattened_repo_list))
    chunked_repos = break_array_into_lists(unique_repo_list, 5000)
    iterator = 1

    for chunked_set in chunked_repos:
        custom_list_name = f'{custom_list_name}_{iterator}'
        iterator += 1

        if len(chunked_set) > 0:
            utils.cacher.write_project_data_to_file(chunked_set, custom_list_name)

def run_search_term():
    # python3 get_repos_from_github.py search_term <SEARCH_TERM>          <LANGUAGE> <CUSTOM_LIST_NAME>
    # python3 get_repos_from_github.py search_term 123 javascript testing-cache123
    print("Finding repos based on a search term")
    search_term = get_argument(2)
    language = get_argument(3)
    custom_list_name = get_argument(4)
    repo_list = []

    github = utils.github_api.create()

    for date_range in utils.github_dates.generate_dates():
        search_term = f'stars:>5 language:{language} fork:false created:{date_range} {search_term}'
        repo_list.append(utils.github_api.get_repos(github, search_term))

    save_repos_to_cached_file(repo_list, custom_list_name)


def run_stars_count():
    # python3 get_repos_from_github.py stars_count <MIN_STARS>            <LANGUAGE> <CUSTOM_LIST_NAME>
    # python3 get_repos_from_github.py stars_count 10000 ruby testing-star-count
    print("Finding repos based on star count")

    min_stars = get_argument(2)
    language = get_argument(3)
    custom_list_name = get_argument(4)
    repo_list = []

    github = utils.github_api.create()

    for date_range in utils.github_dates.generate_dates():
        search_term = f'stars:>{min_stars} created:{date_range} fork:false sort:stars language:{language}'
        repo_list.append(utils.github_api.get_repos(github, search_term))

    save_repos_to_cached_file(repo_list, custom_list_name)


def run_ghtopdep():
    # python3 get_repos_from_github.py ghtopdep    <GITHUB_REPO_URL>              <CUSTOM_LIST_NAME>
    # python3 get_repos_from_github.py ghtopdep https://github.com/expressjs/vhostess testing-ghtopdep
    print("Finding repos based on the ghtopdep tool")

    github_repo_url = get_argument(2)
    custom_list_name = get_argument(3)

    default_ghtopdep_path = "/Users/hacker/Programming/hacking/research/codeql/ghtopdep"
    ghtopdep_path = os.getenv("GHTOPDEP_TOOL_PATH") or default_ghtopdep_path

    # Run ghtopdep
    print("running ghtopdep")
    run_bash_command(f'python3 {ghtopdep_path}/runner.py {github_repo_url} --output_file_name {custom_list_name}')
    print("ghtopdep finished!")


def run_bash_command(command: str):
    split_command = command.split(" ")
    os.system(command)

command = get_argument(1)

if command == "search_term":
    run_search_term()
elif command == "stars_count":
    run_stars_count()
elif command == "ghtopdep":
    run_ghtopdep()
else:
    print("Please provide a valid command.")
    exit()



# based on the arguments, we then run the appropriate script
# gathering either github or ghtopdep data. DO NOT work with
# lgtm at this step.
#
# => 1. determine appropriate script
# => 2. run github or ghtopdep script
# => 3. save script of urls to cache file(s) parsing cached files
#       to always contain less than 5000 repos


# take cache files and follows repos on lgtm.
#
# => 1. (guard clause) first need to check followed repos count on lgtm.
# =>    if too many projects followed, stop script and report that it can't move forward
# => 2. take cached file and move to custom list.
# => 3. unfollowed repos moved to custom list.
