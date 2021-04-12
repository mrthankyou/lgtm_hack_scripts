from lgtm import LGTMSite, LGTMRequestException, LGTMDataFilters, SimpleProject

# This is very similar to SimpleProject. If I had discovered SimpleProject earlier
# I would have built this code around that.
class ProjectBuild(SimpleProject):
    def build_successful(self) -> bool:
        if self.is_protoproject():
            # A throttle that although may not be necessary a nice plus.
            time.sleep(2)
            site = LGTMSite.create_from_file()
            data = site.retrieve_project(self.display_name)

            # A failed protoproject build will always be intrepreted to LGTM as a project that can't be found.
            if 'code' in data and data['code'] == 404:
                return False

            # In this case, the protoproject likely succeeded. To confirm this,
            # we check the language status to confirm the build succeeded.
            for language in data['languages']:
                if language['status'] == "success":
                    self.key = data['id']
                    return True

        return not self.build_in_progress() and not self.build_failed()

    def build_in_progress(self) -> bool:
        return self.project_state("build_attempt_in_progress")

    def build_failed(self) -> bool:
        return self.project_state("build_attempt_failed")

    def project_state(self, state: str) -> bool:
        in_state = False

        if not self.is_valid_project:
            continue

        if self.is_protoproject() and self.state == state:
            in_state = True
            return in_state

        # Real projects always have successful builds, or at least as far as I can tell.
        if not self.is_protoproject():
            in_state = not (state == "build_attempt_in_progress" or state == "build_attempt_failed")
            return in_state

        return in_state

    # def project_currently_followed(self, followed_projects: List[dict]) -> bool:
    #     currently_followed = False
    #     for project in followed_projects:
    #         simple_project = LGTMDataFilters.build_simple_project(project)
    #
    #         if not simple_project.is_valid_project:
    #             continue
    #
    #         if simple_project.display_name == self.display_name:
    #             currently_followed = True
    #             break
    #
    #     return currently_followed
