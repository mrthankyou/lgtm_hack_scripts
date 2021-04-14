- need to see how many projects im currently following on lgtm.
- what custom lists do i currently have
- how do i go about getting all the repos to a lgtm custom list.


1. Access ghtopdep folder  
2. `python3 runner.py <REPO_URL> --minstar 50 --output_file_name <OUTPUT_FILE_NAME_WITHOUT_EXTENSION>`
3. Access lgtm_hack_scripts folder and make sure you're on `network_dependencies_feature` branch.
4. `python3 follow_repos_from_ghtopdep.py <FILE_PATH_TO_GHTOPDEP_OUTPUT>`
5. `python3 move_all_repos_to_lgtm_lists.py <CUSTOM_LIST_NAME>`



- [X] python3 follow_repos_from_ghtopdep.py /root/tools/ghtopdep/cache/flask-mongoengine-ghtopdep-results-0.json  

- [x] python3 follow_repos_from_ghtopdep.py /root/tools/ghtopdep/cache/mongoengine-ghtopdep-results-0.json

- [x] python3 follow_repos_from_ghtopdep.py /root/tools/ghtopdep/cache/flask-pymongo-ghtopdep-results-0.json      

- [ ] python3 follow_repos_from_ghtopdep.py /root/tools/ghtopdep/cache/pymongo-ghtopdep-results-0.json













python3 runner.py https://github.com/MongoEngine/mongoengine --minstar 1 --output_file_name mongoengine-ghtopdep-results-1-star

python3 runner.py https://github.com/mongodb/mongo-python-driver --minstar 1 --output_file_name pymongo-ghtopdep-results-1-star

python3 runner.py https://github.com/dcrosta/flask-pymongo --minstar 1 --output_file_name flask-pymongo-ghtopdep-results-1-star

python3 runner.py https://github.com/MongoEngine/flask-mongoengine --minstar 1 --output_file_name flask-mongoengine-ghtopdep-results-1-star



---------------- TODO

- [ ] python3 follow_repos_from_ghtopdep.py /root/tools/ghtopdep/cache/flask-mongoengine-ghtopdep-results-1-star.json  

- [ ] python3 follow_repos_from_ghtopdep.py /root/tools/ghtopdep/cache/mongoengine-ghtopdep-results-1-star.json

- [ ] python3 follow_repos_from_ghtopdep.py /root/tools/ghtopdep/cache/flask-pymongo-ghtopdep-results-1-star.json      

- [ ] python3 follow_repos_from_ghtopdep.py /root/tools/ghtopdep/cache/pymongo-ghtopdep-results-1-star.json
