## I believe this is a deprecated script in favor of move_cached_repos_to_lgtm_lists.py

# python3 move_repos_to_lgtm.py <CACHE_FILE_NAME>(optional)

from typing import List
from lgtm import LGTMSite, LGTMDataFilters, LGTMRequestException

import os
import sys
import json
import time
import numpy
import shutil
import subprocess
import utils.github_api
import utils.github_dates
from models import ProjectBuilds, ProjectBuild

def create_project_build(simple_project: SimpleProject):
    return ProjectBuild(
        display_name=simple_project.display_name,
        key=simple_project.key,
        project_type=simple_project.project_type,
        is_valid_project=True,
        org="",
        state=""
    )

def follow_projects_on_lgtm(site: 'LGTMSite', projects: List[str]) -> List[ProjectBuild]:
    followed_projects = []

    for repo_name in projects:
        saved_project = save_project_to_lgtm(site, repo_name)

        simple_project = LGTMDataFilters.build_simple_project(saved_project)

        if not simple_project.is_valid_project:
            continue

        project_build = create_project_build(simple_project)
        followed_projects.append(project_build)

    return newly_followed_projects


def move_repos_to_custom_list(site: 'LGTMSite', project_builds: ProjectBuilds, custom_list_name: str):
    project_list_id = site.get_or_create_project_list(custom_list_name)

    print(f"Moving followed projects to the {custom_list_name} list")
    successful_builds = project_builds.return_successful_project_builds(site)
    site.load_into_project_list(project_list_id, successful_builds)

def unfollow_repos_moved_to_custom_list(project_builds: ProjectBuilds):
    print("Unfollowing projects")
    # If a project fails to be processed by LGTM, we still unfollow the project.
    project_builds.unfollow_projects(site)

def run_initial_checks(site: 'LGTMSite'):
    try:
        current_followed_projects = site.get_my_projects()
    except LGTMRequestException:
        print("We're getting exceptions from LGTM.com. Halting script.")
        exit()

    if not len(current_followed_projects) > 5000:
        return

    print("You are following too many projects in your LGTM account. Please move these repos to custom lists to make sure you don't brick your LGTM account.")
    exit()

def run(site: 'LGTMSite', projects: List[ProjectBuild], custom_list_name: str):
    followed_projects = follow_projects_on_lgtm(site, projects)

    project_builds = ProjectBuilds(followed_projects)

    if project_builds.build_processes_in_progress():
        print(f'The {cached_file_name} can\'t be processed at this time because a project build is still in progress.')
        exit()

    move_repos_to_custom_list(site, project_builds)
    unfollow_repos_moved_to_custom_list(project_builds)

def process_cached_file(site: 'LGTMSite', cached_file_name: str):
    project_builds = utils.cacher.get_project_builds(cached_file_name)
    custom_list_name = cached_file_name.split(".")[0]
    run(site, project_builds, custom_list_name)
    utils.cacher.remove_file(cached_file_name)

user_selected_cached_file_name = sys.argv[1]
site = LGTMSite.create_from_file()
run_initial_checks(site)


if user_selected_cached_file_name:
    process_cached_file(site, user_selected_cached_file_name)
    print("finished!")
    exit()


for cached_file_name in os.listdir("cache"):
    process_cached_file(site, cached_file_name)
print("finished!")
