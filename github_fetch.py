#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:15:48 2017

@author: tania
This python script is used to extract the data from the GitHub pull requests
"""


# Loading the required packages 
import requests
import json
import sys
from urllib.parse import urljoin


# Info needed to construct the API get request
gh_user = 'RSE-Sheffield'
gh_repo = 'RSE-Sheffield.github.io'


construct = {'baseurl': 'https://api.github.com/repos/', 
             'pulls': gh_user + '/' + gh_repo + '/pulls',
             'issues': gh_user + '/' +  gh_repo + '/issues'}

#---------------------------------------------------------
def create_url(request):
    url = urljoin(construct['baseurl'], construct[request])
    return url
    
    
def get_pulls(*state):
    """ Gets the pull requests in the specified repo"""
    
    url = create_url('pulls')
    
    if not state:
        state = 'open'
        
    response = requests.get(url, params = {'state': state})

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return "Error: " + str(e)

    # Must have been a 200 status code
    response_json = response.json()
    return response_json


def get_files(pulls):
    """ Gets the latest pull request from the repository and identify the
    files modified/ added """
    
     
    # note the first element corresponds to the latest pull request
    construct['pull_no'] = str(pulls[0]['number'])
    construct['last_pull'] = construct['pulls'] + '/' + construct['pull_no'] 
    construct['pull_files'] = construct['pulls'] + '/' + construct['pull_no'] + '/files'
     
    url = create_url('pull_files')
    
    response = requests.get(url)
    response_json = response.json()
    
    return response_json


def get_lissue():
    """Getting the issue that correspond to the pull request """
    
    construct['last_issue'] = construct['issues'] + '/' +  construct['pull_no']
    
    url = create_url('last_issue')
 
    response = requests.get(url)
    response_json = response.json()
    return response_json


def get_revcom():
    """Get the comments from the reviewers"""
    construct['comments'] = construct['last_pull'] + '/comments'
    
    url = create_url('comments')
    response = requests.get(url)
    response_json = response.json()
    return response_json
    
def summarise_info(PR):
        
    """ Saves the data collected """
    PR_info = {'author' : PR['user']['login'],
               'created_at': PR['created_at'],
               'commit_sha': PR['head']['sha']}
    
    
    # Getting the assigned revieswers 
    reviewer_ind = get_reviewers(PR)    
    PR_info['reviewers'] = reviewer_ind
    
    # Getting the reviewers comments
    
    if not PR['merged_at']: 
        print('*** This PR has not been merged yet ***')
    else:
        comments = get_revcom()
        PR['merged_at'] = PR['merged_at']
        comment_ind = dict_comments(PR)
        PR_info['rev_comments'] = comment_ind
    
    return PR_info

def get_reviewers(PR):
    """ Get the reviewers assigned """
    rev_keys = ['login','html_url']
    for i in PR['requested_reviewers']:
        reviewer_ind = {k:i[k] for k in rev_keys}
    
    return reviewer_ind

def dict_comments(PR):
    """Summarise the comments"""
          
    com_keys = ['body', 'diff_hunk']
    for i in comments:
        comment_ind = {k:i[k] for k in wanted}
        comment_ind['User'] = i['user']['login']
    
    return comment_ind
        
#---------------------------------------------------------

# First we need to get the PR
pulls = get_pulls('all')

# Identify the files from the last pull request
pulls_files = get_files(pulls)

# Summarising the information for the last PR
PR = pulls[0]
PR_info = summarise_info(PR)

# Saving the info
json.dump(PR_info, open('./PR_summary.json', 'w'))


