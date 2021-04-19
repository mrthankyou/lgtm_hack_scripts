# THIS SCRIPT WILL TAKE ALL FOLLOWED PROJECTS ON LGTM AND MOVE THEM INTO A CUSTOM LIST.
# THIS IS USEFUL IF YOU ARE USING THIS SCRIPT ALONGSIDE THE  follow_repos_from_ghtopdep.py
# SCRIPT WHICH WILL SIMPLY TAKE THE RESULTS OF THE GHTOPDEP TOOL AND THEN FOLLOW THEM ON
# LGTM.COM WITHOUT PASSING TO A CUSTOM LIST. ANOTHER WAY TO PUT IT, THIS SCRIPT MOVES
# ALL THOSE REPOS TO A CUSTOM LIST.

# python3 move_all_repos_to_lgtm_lists.py <CUSTOM_LIST_NAME>

from typing import List
from lgtm import LGTMSite, LGTMDataFilters
# from utils.cacher import ProjectBuild, ProjectBuilds
from models import ProjectBuild, ProjectBuilds
# import models.ProjectBuild
# import models.ProjectBuilds
# import models

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

if project_builds_class.build_processes_in_progress():
    print(f'Some projects are still being processed or have failed. Ignoring these projects for now.')
    exit

print("adding to list")
successful_builds = project_builds_class.return_successful_project_builds(site)
site.load_into_project_list(project_list_id, successful_builds)

print("unfollowing projects")
project_builds_class.unfollow_projects(site)
