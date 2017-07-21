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

def get_reviewers():
    """Getting the review information for the PR"""
    
    construct['reviewers'] = construct['last_pull'] + '/requested_reviewers'
    
    url = create_url('reviewers')
    response = requests.get(url)
    response_json = response.json()
    return response_json

def get_rcom():
    construct['comments'] = construct['last_pull'] + '/comments'
    
    url = create_url('comments')
    response = requests.get(url)
    response_json = response.json()
    return response_json
    
#---------------------------------------------------------

# getting pull requests: all, closed, open
pulls = get_pulls('all')

pulls_files = get_files(pulls)

last_issue = get_lissue()
