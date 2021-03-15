from typing import List
from lgtm import LGTMSite

import utils.cacher
import os
import sys


def process_cached_file(cached_file_name: str, site: 'LGTMSite'):
    cached_file = cached_file_name
    project_builds = utils.cacher.get_project_builds(cached_file)

    # If a project fails to be processed by LGTM, we still unfollow the project.
    print("Unfollowing projects")
    project_builds.unfollow_projects(site)
    print("Removing the cache file.")
    print("Done processing cache file.")

site = LGTMSite.create_from_file()

if len(sys.argv) > 1:
    user_selected_cached_file = sys.argv[1]
else:
    user_selected_cached_file = None

if user_selected_cached_file:
    process_cached_file(f'cache/{user_selected_cached_file}', site)
else:
    for cached_file_name in os.listdir("cache"):
        process_cached_file(f'cache/{cached_file_name}', site)

print("Finished!")
