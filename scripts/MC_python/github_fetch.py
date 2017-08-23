#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:15:48 2017

@author: tania
This python functions are used to extract the data from the GitHub pull requests
it uses the Github API v3
note that you might need to authenticate to complete some if this actions
"""

# Loading the required packages
import requests
import json
import sys
from urllib.parse import urljoin
import yaml
from MC_python import *


construct = {'baseurl': 'https://api.github.com/repos/',
             'pulls': gh_user + '/' + gh_repo + '/pulls',
             'issues': gh_user + '/' + gh_repo + '/issues'}


# ---------------------------------------------------------
# The following are the various methods used to query
# data from GitHub and format data 



def create_url(request):
    url = urljoin(construct['baseurl'], construct[request])
    return url


def get_pulls(*state):
    """ Gets the pull requests in the specified repo"""

    url = create_url('pulls')

    if not state:
        state = 'open'

    response = requests.get(url, params={'state': state})

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        # Whoops it wasn't a 200
        error_details = error.read()
        error_details = json.loads(error_details.decode('utf-8'))
        
        if error.code in http_error_messages:
            sys.exit(http_error_messages[error.code])
        else:
            error_message = 'ERROR: There was a problem processing your request {}:{}'.format(error.code, error.reason)
            if'message' in error_details:
                error_message += "\n Details: " + error_details['message']
            sys.exit(error_message)
            
        #return "Error: " + str(e)

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

    construct['last_issue'] = construct['issues'] + '/' + construct['pull_no']

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
    PR_info = {'number' : PR['number'],
               'author': PR['user']['login'],
               'created_at': PR['created_at'],
               'commit_sha': PR['head']['sha']}
   
    if not PR['requested_reviewers']:
        print('*** Reviewers have not been assigned yet *** \n\n')
    else:
        # Getting the assigned reviewers
        reviewer_ind = get_reviewers(PR)
        PR_info['reviewers'] = reviewer_ind

    # Getting the reviewers comments

    if not PR['merged_at']:
        print('*** This PR has not been merged yet *** \n\n')
    else:
        comments = get_revcom()
        PR['merged_at'] = PR['merged_at']
        comment_ind = dict_comments(PR)
        PR_info['rev_comments'] = comment_ind

    return PR_info


def get_reviewers(PR):
    """ Get the reviewers assigned """
    rev_keys = ['login', 'html_url']
    for i in PR['requested_reviewers']:
        reviewer_ind = {k: i[k] for k in rev_keys}

    return reviewer_ind


def dict_comments(PR):
    """Summarise the comments"""

    com_keys = ['body', 'diff_hunk']
    for i in comments:
        comment_ind = {k: i[k] for k in wanted}
        comment_ind['User'] = i['user']['login']

    return comment_ind



def import_PR(issue):
    """ This imports the issue associated to the PR submission
    and returns a template that will be used to populate
    the template"""
    
    template_data = {}
    template_data['author'] = issue.user.login
    template_data['author_url'] = issue.user.html_url
    template_data['author_avatar'] = issue.user.avatar_url
    template_data['author_name'] = Github.user(issue.user.login).name
    template_data['body'] = issue.body
    template_data['repo'] = issue.pull_request().head.as_dict()['repo']['url']
    return template_data


def format_PR(template_data):
    """ This applies the PR template to the submitted PR"""
    
    from string import Template
    
    loc = os.path.join(os.path.split(os.getcwd())[0], 'templates/PR_template.md')
    
    template_file = open(loc, 'r')
    template = Template(template_file.read())
    return template.substitute(template_data)
    
# ---------------------------------------------------------
class state:
	current = ""
	INITIALIZING         = "script-initializing"
	LOADING_CONFIG       = "loading-config"
	FETCHING_ISSUES      = "fetching-issues"
	GENERATING           = "generating"
	IMPORT_CONFIRMATION  = "import-confirmation"
	IMPORTING            = "importing"
	IMPORT_COMPLETE      = "import-complete"
	COMPLETE             = "script-complete"
	
state.current = state.INITIALIZING

http_error_messages = {}
http_error_messages[401] = "ERROR: There was a problem during authentication.\nDouble check that your username and password are correct, and that you have permission to read from or write to the specified repositories."
http_error_messages[403] = http_error_messages[401]; # Basically the same problem. GitHub returns 403 instead to prevent abuse.
http_error_messages[404] = "ERROR: Unable to find the specified repository/source requested.\nDouble check the spelling for the source and target repositories. If either repository is private, make sure the specified user is allowed access to it."


# ---------------------------------------------------------

# Updating or formatting issues and PR

def update_PR(PR, data):
    """ Used to change the body of the PR according to a
    predefined template """
    # note the first element corresponds to the latest pull request
    construct['pull_no'] = str(pulls[0]['number'])
    construct['last_pull'] = construct['pulls'] + '/' + construct['pull_no']

    url = create_url('last_pull')

    update =  requests.patch(url, data)
    
        
    

def format_from_template(template, template_data):
    from string import Template
    loc = os.path.join(os.getcwd(), 'templates')
    template_file = open(template, 'r')
    temp = Template(template_file.read())
    return template.substitute(template_data)
        
    

# labels 
# colors (blue,     dark-grey,  red,        green)
colors = ['#1F618D', '#283747', '#B03A2E', '#1E8449']

labels = {'review' : '1F618D'}