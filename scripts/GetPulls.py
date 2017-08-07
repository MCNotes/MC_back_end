#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 13:58:57 2017

@author: tania
his python script is used to extract the data from the GitHub pull requests
it uses the Github API v3
note this is not using OAuth as it is not intented for POST request
or to exceed 60 requests per hour

This uses the github3 library as a wrapper for the Gtihub API
"""

import github3 as gh3
import yaml
from MC_python import *

# get the repository to use from the package
repo = gh3.repository(gh_user, gh_repo)

"""  We will collate the issues and identify if they
are PR as all PR are issues but not viceversa"""


issues = []
PRs = []

# getting only open issues 

for issue in repo.issues(state ='open'):
    issues.append(issue)
    PR = issue.pull_request()
    try: 
        PR.is_null()
    except:
        PRs.append(PR)

# only focusing on the last PR
last_pull = PRs[0]


# getting the files of the last PR
files = []

for file in last_pull.files():
    files.append(file.filename)


# Now we save the info in a dictionary structure
PR_info  = {'author' : last_pull.user.login,
            'created_at': last_pull.created_at.strftime('%d/%m/%Y'),
            'number' : last_pull.number,
            'files' : files}

with open('PR_summary.yml', 'w') as yml_file:
    yaml.dump(PR_info, yml_file, default_flow_style = False)
