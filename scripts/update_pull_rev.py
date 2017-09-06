#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 13:58:57 2017

@author: Tania Allard
@github user: trallard

This Python script modifies the Pull request template and changes the label for the intial review of the notebooks. 

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


# get the repository to use from the package
repo = gh3.repository(gh_user, gh_repo)
issue = repo.issue( PR_info['number'])

def import_PR(issue):
    template_data = {}
    template_data['user'] = issue.user.login
    template_data['user_url'] = issue.user.html_url
    template_data['user_avatar'] = issue.user.avatar_url
    return template_data

def format_PR(template_data):
    """ This applies the PR template to the submitted PR"""
    from string import Template
    
    loc = os.path.join(os.getcwd(), 'templates')
    loc = os.path.join(os.path.split(os.getcwd())[0], 'templates/PR_template.md')
    
    template_file = open(loc, 'r')
    template = Template(template_file.read())
    return template.substitute(template_data)

template_data = import_PR(issue)

dummy = format_PR(template_data)


def update_PR(PR, data):
    """ Used to change the body of the PR according to a
    predefined template """
    # note the first element corresponds to the latest pull request
    construct['pull_no'] = str(pulls[0]['number'])
    construct['last_pull'] = construct['pulls'] + '/' + construct['pull_no']

    url = create_url('last_pull')


    update =  requests.patch(url, data)
    
    
   
    
    
# labels 
         
labels = {'pre-review' : '1F618D',
           'review' : '283747',
           'revision-interrupted':'B03A2E',
           'everything-OK': '1E8449' }        
         
         
         