#!/usr/bin/env python3
"""Refresh project metadata in data/projects.yml from GitHub."""
import sys
from os import getenv

import requests
import yaml


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("provide path to projects.yml")

    api_token = getenv("GITHUB_TOKEN")
    if not api_token:
        sys.exit("GITHUB_TOKEN is missing")

    headers = {"Authorization": f"Bearer {api_token}"}

    with open(sys.argv[1], encoding="utf-8") as stream:
        try:
            projects = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            sys.exit(exc)

    for project in projects:
        repo = project.get("github_uri")
        if not repo:
            continue
        print(repo)

        url = f"https://api.github.com/repos/{repo}"
        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code in [401, 403, 429]:
            sys.exit(f"GitHub API denied the request: HTTP {r.status_code}")
        elif r.status_code != 200:
            print(f"skipping {repo}: HTTP {r.status_code}")
            continue

        data = r.json()

        # Update URLs.
        project["name"] = data["name"]
        project["url"] = f"https://github.com/{repo}"

        if data["description"]:
            project["description"] = data["description"]

        project["language"] = data["language"]

        if data["license"] and "name" in data["license"]:
            project["license"] = data["license"]["name"]

        project["topics"] = data["topics"]
        project["stars"] = data["stargazers_count"]
        project["updated_at"] = data["pushed_at"]

    with open(sys.argv[1], "w", encoding="utf-8") as f:
        yaml.safe_dump(projects, f)
