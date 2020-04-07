#!/bin/python
"""
This script reads the Hugo data/projects.json lists file, fetches the Github
project metadata and updates the file.
"""
import sys
import yaml
import json
import requests
from requests.auth import HTTPBasicAuth

def fetch_project(url):
    pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("provide path to projects.yml")

    # Source: https://stackoverflow.com/a/1774043
    with open(sys.argv[1], 'r') as stream:
        try:
            projects = (yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            sys.exit(exc)
    
    for i, p in enumerate(projects):
        if "github_uri" not in p:
            continue

        print(p["github_uri"])
        r = requests.get("https://api.github.com/repos/{}".format(p["github_uri"]))
        # auth=HTTPBasicAuth("", ""))
        data = json.loads(r.content)

        # Update URLs.
        projects[i]["name"] = data["name"]
        projects[i]["url"] = "https://github.com/" + p["github_uri"]
        projects[i]["description"] = data["description"]
        projects[i]["stars"] = data["stargazers_count"]
        projects[i]["updated_at"] = data["updated_at"]
    with open(sys.argv[1], "w") as f:
        f.write(json.dumps(projects, indent=2))