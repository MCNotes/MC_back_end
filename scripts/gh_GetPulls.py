#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Tania Allard
@ghuser: trallard

This python script is used to extract the data from the GitHub pull requests
note this is not using OAuth as it is not processing POST request
or to exceed 60 requests per hour.
"""

# getting the location of the script and changing the wd
import os 

wk_dir = os.path.dirname(os.path.realpath('__file__'))
os.chdir(wk_dir)

# Loading the required packages

from MC_python import github_fetch as gh
import json
import yaml

#---------------------------------------------------------
# getting the location of the script and changing the wd

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


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

# Saving the information obtained
#in json format
#json.dump(PR_info, open('./PR_summary.json', 'w'))

# Saving the information obtained in yaml format
with open('PR_summary.yml', 'w') as yml_file:
    yaml.dump(PR_info, yml_file, default_flow_style = False)


