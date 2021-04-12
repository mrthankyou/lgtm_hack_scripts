- need to see how many projects im currently following on lgtm.
- what custom lists do i currently have
- how do i go about getting all the repos to a lgtm custom list.


1. Access ghtopdep folder  
2. `python3 runner.py <REPO_URL> --minstar 50 --output_file_name <OUTPUT_FILE_NAME_WITHOUT_EXTENSION>`
3. Access lgtm_hack_scripts folder and make sure you're on `network_dependencies_feature` branch.
4. `python3 follow_repos_from_ghtopdep.py <FILE_PATH_TO_GHTOPDEP_OUTPUT>`
5. `python3 move_all_repos_to_lgtm_lists.py <CUSTOM_LIST_NAME>`


/root/tools/ghtopdep/cache


flask-mongoengine-ghtopdep-results-0.json  
mongoengine-ghtopdep-results-0.json
flask-pymongo-ghtopdep-results-0.json      
pymongo-ghtopdep-results-0.json
