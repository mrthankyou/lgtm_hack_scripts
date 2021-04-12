from typing import List
import os
import time
from lgtm import LGTMSite, LGTMRequestException, LGTMDataFilters, SimpleProject
from models import ProjectBuild, ProjectBuilds

# put project build and project builds back in here when done

def create_cache_folder():
    if not os.path.exists('cache'):
        os.makedirs('cache')

def write_project_data_to_file(project_keys: List[str], file_name: str):
    create_cache_folder()

    file = open("cache/" + file_name + ".txt", "a")

    for project_key in project_keys:
        file.write(project_key + "\n")

    file.close()

def get_project_builds(cached_file: str) -> ProjectBuilds:
    file = open(cached_file, "r")

    cached_projects = file.read().split("\n")

    while("" in cached_projects):
        cached_projects.remove("")

    for i, project in enumerate(cached_projects):
        cached_projects[i] = ProjectBuild(
            display_name=project.split(",")[0],
            key=project.split(",")[1],
            project_type=project.split(",")[2],
            is_valid_project=True,
            org="",
            state=""
        )

    file.close()

    return ProjectBuilds(cached_projects)

def remove_file(file_name: str):
    os.remove(file_name)
