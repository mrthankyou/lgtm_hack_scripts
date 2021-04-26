from lgtm import LGTMSite, LGTMRequestException, LGTMDataFilters, SimpleProject
from models import ProjectBuild

class ProjectBuilds:
    def __init__(self, projects: List[ProjectBuild]):
        self.projects = projects

    def unfollow_projects(self, site: 'LGTMSite'):
        for project in self.projects:
            time.sleep(1)

            if project.is_protoproject():
                # Protoprojects are gnarly because I believe LGTM updates the key
                # if the protoproject succeeds. In case it does, we retrieve the
                # latest id from LGTM then unfollow it.
                data = site.retrieve_project(project.display_name)

                # A failed protoproject build will be intrepreted to LGTM
                # as a project that can't be found.
                if 'code' in data and data['code'] == 404:
                    continue

                self.unfollow_proto_project(site, data['id'])
            else:
                self.unfollow_real_project(site, project.key)


    def unfollow_proto_project(self, site: 'LGTMSite', id: int):
        try:
            time.sleep(1)

            site.unfollow_proto_repository_by_id(id)
        except LGTMRequestException as e:
            # In some cases even though we've recorded the project as a protoproject
            # it's actually a realproject. So we can't unfollow it via a proto-project
            # unfollow API call. We can however unfollow it via the real project API call.
            self.unfollow_real_project(site, id)

    def unfollow_real_project(self, site: 'LGTMSite', id: int):
        try:
            time.sleep(1)

            site.unfollow_repository_by_id(id)
        except LGTMRequestException as e:
            print(f"An unknown issue occurred unfollowing {id}")

    def return_successful_project_builds(self, site: 'LGTMSite') -> List[str]:
        filtered_project_keys: List[str] = []
        followed_projects = site.get_my_projects()

        for project in self.projects:
            if project.build_successful(followed_projects):
                filtered_project_keys.append(project.key)

        return filtered_project_keys

    def build_processes_in_progress(self) -> bool:
        in_progress = False

        for project in self.projects:
            if project.build_in_progress:
                in_progress = True
                break

        return in_progress
