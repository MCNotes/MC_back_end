#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:15:48 2017

@author: Tania Allard
@ghuser: trallard

This python script is used to extract the data from the GitHub pull requests
it uses the Github API v3
note this is not using OAuth as it is not intented for POST request
or to exceed 60 requests per hour
"""


# Loading the required packages

from MC_python import *
from MC_python import github_fetch as gh
import requests
import json
import sys
from urllib.parse import urljoin
import yaml


#---------------------------------------------------------

# First we need to get the PR
pulls = gh.get_pulls('open')

# Identify the files from the last pull request
pulls_files = gh.get_files(pulls)
files = []
for file in pulls_files:
    files.append(file['filename'])

# Summarising the information for the last PR
PR = pulls[0]
PR_info = gh.summarise_info(PR)

PR_info['files'] = files

# Saving the info
json.dump(PR_info, open('./PR_summary.json', 'w'))
with open('PR_summary.yml', 'w') as yml_file:
    yaml.dump(PR_info, yml_file, default_flow_style = False)


