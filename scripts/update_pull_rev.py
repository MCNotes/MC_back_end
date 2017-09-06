#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 13:58:57 2017

@author: Tania Allard
@github user: trallard

This Python script modifies the Pull request template and changes the label 
for the intial review of the notebooks. 

This uses the github3 library as a wrapper for the Gtihub API
"""

import github3 as gh3
import yaml
from MC_python import *
from MC_python import github_fetch as gh
import os


# Read YAML file with the pull request info
with open("PR_summary.yml", 'r') as stream:
    PR_info = yaml.load(stream)

# since we will be updating the PR we need to open an authenticated session
Github = gh3.login(token = token)
print('*** The PR will be modified by {} *** \n\n\n' .format(Github.me()))

# get the repository to use from the package
issue = Github.issue(gh_user, gh_repo, PR_info['number'])

# we collect the information needed from the author and the repo
template_data = import_PR(issue)

# and reformat the PR using our custom template
dummy = format_PR(template_data)

# setting the approriate label
PR_labs = issue.add_labels('review')
PR_labs[-1].update(PR_labs[-1].name, color[1])

# applying the template
update_PR(issue, dummy)

def update_PR(issue, content):
    edited_PR = issue.edit(title = issue.title, body = content)
    return edited_PR
    
    
# labels 
         
labels = {'pre-review' : '1F618D',
           'review' : '283747',
           'revision-interrupted':'B03A2E',
           'everything-OK': '1E8449' }        
         
         
         