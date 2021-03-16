from typing import List
from github import Github
import yaml
import time


def create() -> Github:
    with open("config.yml") as config_file:
        config = yaml.safe_load(config_file)
        github: dict = config['github']
        return Github(github['api_key'])

def get_repos(github: Github, search_term: str) -> List[str]:
    saved_project_data: List[str] = []

    repos = github.search_repositories(query=search_term)

    # TODO: This occasionally returns requests.exceptions.ConnectionError which is annoying as hell.
    # It would be nice if we built in exception handling.
    for repo in repos:
        # Github has rate limiting in place hence why we add a sleep here. More info can be found here:
        # https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting
        time.sleep(1)

        if repo.archived or repo.fork:
            continue

        saved_project_data.append(repo.full_name)

    return saved_project_data
