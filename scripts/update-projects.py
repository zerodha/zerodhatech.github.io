#!/bin/python
"""
This script reads the Hugo data/projects.json lists file, fetches the Github
project metadata and updates the file.
"""
import sys
import yaml
import json
import requests
from os import getenv
from requests.auth import HTTPBasicAuth


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("provide path to projects.yml")

    api_token = getenv("GITHUB_TOKEN", "")
    if not api_token:
        sys.exit("GITHUB_TOKEN is missing")

    headers = {"Authorization": "token %s" % api_token}

    # Source: https://stackoverflow.com/a/1774043
    with open(sys.argv[1], "r") as stream:
        try:
            projects = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            sys.exit(exc)

    for i, p in enumerate(projects):
        if "github_uri" not in p:
            continue
        print(p["github_uri"])


        url = "https://api.github.com/repos/{}".format(p["github_uri"])
        r = requests.get(url, headers=headers)

        if r.status_code in [401, 403, 429]:
            sys.exit("unauthorized or rate limited: {}".format(r.status_code))
        elif r.status_code != 200:
            print("skipping {}: bad status code: {}".format(p["github_uri"], r.status_code))
            continue

        data = json.loads(r.content)

        # Update URLs.
        projects[i]["name"] = data["name"]
        projects[i]["url"] = "https://github.com/" + p["github_uri"]

        if data["description"]:
            projects[i]["description"] = data["description"]

        projects[i]["language"] = data["language"]

        if data["license"] and "name" in data["license"]:
            projects[i]["license"] = data["license"]["name"]

        projects[i]["topics"] = data["topics"]
        projects[i]["stars"] = data["stargazers_count"]
        projects[i]["updated_at"] = data["pushed_at"]

    with open(sys.argv[1], "w") as f:
        yaml.dump(projects, f)
