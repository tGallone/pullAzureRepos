#! /usr/local/bin/python3
import os
from msrest.authentication import BasicAuthentication
from azure.devops.connection import Connection
AZURE_PERSONAL_ACCESS_TOKEN = '<YOUR_PERSONAL_ACCESS_TOKEN>'
AZURE_ORGANIZATION_URL = 'https://dev.azure.com/<YOUR_ORGANIZATION>'

try:
    connection = Connection(base_url=AZURE_ORGANIZATION_URL, creds=BasicAuthentication('', AZURE_PERSONAL_ACCESS_TOKEN))
    client = connection.clients.get_core_client()
    print("Successfully logged in")
except:
    print("Failed to login")

def clone_repos(project):
    git_client = connection.clients.get_git_client()
    repos = git_client.get_repositories(project.id)
    os.system(f"mkdir {project.name}")
    os.chdir(f"{project.name}")
    for repo in repos:
        if os.path.isdir(repo.name) == True:
            print(f"{repo.name} " "already exists, pulling latest changes")
            os.chdir(f"{repo.name}")
            os.system(f"git pull {repo.web_url}")
        else:
            target_dir = f"{repo.name}"
            os.mkdir(target_dir)
            os.system(f"git clone {repo.web_url} {target_dir}")

get_projects_response = client.get_projects()
counter = 0
for project in get_projects_response.value:
    counter+=1
    clone_repos(project)
else:
    print("Everything has been cloned!")