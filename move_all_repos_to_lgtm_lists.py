from typing import List
from lgtm import LGTMSite, LGTMDataFilters
from utils.cacher import ProjectBuild, ProjectBuilds

import os
import sys

site = LGTMSite.create_from_file()
projects = site.get_my_projects()
project_keys = []

project_list_name = sys.argv[1]
project_list_id = site.get_or_create_project_list(project_list_name)
project_builds = []

for project in projects:
    simple_project = LGTMDataFilters.build_simple_project(project)

    project_build = ProjectBuild(
        display_name=simple_project.display_name,
        key=simple_project.key,
        project_type=simple_project.project_type,
        is_valid_project=simple_project.is_valid_project,
        org=simple_project.org,
        state=simple_project.state
    )

    if not project_build.is_valid_project:
        continue

    project_builds.append(project_build)
    project_keys.append(project_build.key)

project_builds_class = ProjectBuilds(project_builds)

if project_builds_class.build_processes_in_progress(projects):
    print(f'The {cached_file_name} can\'t be processed at this time because a project build is still in progress.')
    exit


# print("adding to list")
# successful_builds = project_builds_class.return_successful_project_builds(site)
# site.load_into_project_list(project_list_id, successful_builds)
# print("unfollowing projects")

project_builds_class.unfollow_projects(site)
print("Finished!")
