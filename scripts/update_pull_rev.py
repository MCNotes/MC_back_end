#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 13:58:57 2017

@author: tania
This Python script modifies the Pull request template and changes the label for the intial review of the notebooks. 

This uses the github3 library as a wrapper for the Gtihub API
"""

import github3 as gh3
import yaml
from MC_python import *
from MC_python import github_fetch as gh


# hard coding for now
gh_user = 'MCNotes'
gh_repo = 'MCNotes.github.io'



# Read YAML file with the pull request info
with open("PR_summary.yml", 'r') as stream:
    PR_info = yaml.load(stream)


# get the repository to use from the package
repo = gh3.repository(gh_user, gh_repo)

