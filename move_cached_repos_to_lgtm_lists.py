# I'm assuming this is the script i want to use to convert cached projects to a custom list.
# python3 move_cached_repos_to_lgtm_lists.py

from typing import List
from lgtm import LGTMSite

import utils.cacher
import os

def get_project_list_id(cached_file_name: str, site: 'LGTMSite') -> str:
    project_list_name = cached_file_name.split(".")[0]

    return site.get_or_create_project_list(project_list_name)

def process_cached_file(cached_file_name: str, site: 'LGTMSite'):
    project_builds = utils.cacher.get_project_builds(cached_file_name)
    followed_projects = site.get_my_projects()

    if project_builds.build_processes_in_progress(followed_projects):
        print(f'The {cached_file_name} can\'t be processed at this time because a project build is still in progress.')
        return

    project_list_id = get_project_list_id(cached_file_name, site)

    print("Moving followed projects to the project list")
    site.load_into_project_list(project_list_id, project_builds.return_successful_project_builds(site))

    # If a project fails to be processed by LGTM, we still unfollow the project.
    print("Unfollowing projects")
    project_builds.unfollow_projects(site)

    # Temporarily commenting this out as I'm having issues following projects and would
    # like to retain the list of cached files
    #
    # print("Removing the cache file.")
    # utils.cacher.remove_file(cached_file_name)
    print("Done processing cache file.")

site = LGTMSite.create_from_file()
user_selected_cached_file = sys.argv[1]

if user_selected_cached_file:
    process_cached_file(f'cache/{user_selected_cached_file}', site)
else:
    for cached_file_name in os.listdir("cache"):
        process_cached_file(f'cache/{cached_file_name}', site)

print("Finished!")
