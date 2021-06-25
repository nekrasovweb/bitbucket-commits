#!/usr/local/bin/python

import os, json, requests, datetime, urllib3
from collections import defaultdict

username = os.environ.get('BB_USER')
password = os.environ.get('BB_PASS')
base_api_url = os.environ.get('BB_API_URL')
path_root_ca = os.environ.get('BB_PATH_CA')
year = 2021


def get_all_items(base_url):
    all_items = []
    r = requests.get(base_url, auth=(username, password), verify=path_root_ca)
    c = r.json()
    if 'values' not in c:
        print(c)  # debug

    all_items.extend(c['values'])
    while not c['isLastPage']:
        r = requests.get("{base}?start={nextPageStart}".format(
            base=base_url,
            nextPageStart=c['nextPageStart']),
            auth=(username, password),
            verify=path_root_ca)
        c = r.json()
        all_items.extend(c['values'])

    return all_items


def it_commits_for_repo(key, slug):
    all_commits = get_all_items("{base}/projects/{key}/repos/{slug}/commits".
                                format(base=base_api_url, key=key, slug=slug))
    print('project key:', key, 'repo_name:', slug, 'size_commit:', all_commits.__len__())


def it_repositories_for_project(key):
    all_repositories = get_all_items("{base}/projects/{key}/repos".format(base=base_api_url, key=key))
    for repository in all_repositories:
        it_commits_for_repo(key, repository['slug'])


def it_projects():
    all_projects = get_all_items("{base}/projects".format(base=base_api_url))
    for project in all_projects:
        it_repositories_for_project(project['key'])


it_projects()
quit()
