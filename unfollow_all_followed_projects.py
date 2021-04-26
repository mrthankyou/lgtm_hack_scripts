import time
from lgtm import LGTMSite, LGTMDataFilters

site = LGTMSite.create_from_file()

projects = site.get_my_projects()

for project in projects:
    simple_project = LGTMDataFilters.build_simple_project(project)
    if simple_project.is_valid_project:
        print("unfollowing project")
        time.sleep(1)
        site.unfollow_repository(simple_project)
