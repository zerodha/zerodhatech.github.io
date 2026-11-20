"""Refresh project metadata in data/projects.yml from GitHub."""

import sys
from argparse import ArgumentParser
from os import getenv
from pathlib import Path

import requests
import yaml


def refresh_projects(projects: list[dict[str, object]], token: str) -> None:
    with requests.Session() as session:
        session.headers.update({"Authorization": f"Bearer {token}"})

        for project in projects:
            repo = project.get("github_uri")
            if not repo:
                continue

            response = session.get(f"https://api.github.com/repos/{repo}", timeout=15)
            if response.status_code == 404:
                print(f"Skipping {repo}: repository not found", file=sys.stderr)
                continue
            response.raise_for_status()
            metadata = response.json()

            project.update(
                name=metadata["name"],
                url=f"https://github.com/{repo}",
                language=metadata["language"],
                topics=metadata["topics"],
                stars=metadata["stargazers_count"],
                updated_at=metadata["pushed_at"],
            )
            if description := metadata.get("description"):
                project["description"] = description
            if license_info := metadata.get("license"):
                if name := license_info.get("name"):
                    project["license"] = name


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("projects", type=Path, help="path to projects.yml")
    path = parser.parse_args().projects
    if not (token := getenv("GITHUB_TOKEN")):
        parser.exit(1, "GITHUB_TOKEN is required to refresh project metadata.\n")

    try:
        projects = yaml.safe_load(path.read_text(encoding="utf-8"))
        refresh_projects(projects, token)
        path.write_text(yaml.safe_dump(projects), encoding="utf-8")
    except (OSError, requests.RequestException, yaml.YAMLError) as error:
        parser.exit(1, f"Could not refresh {path}: {error}\n")


if __name__ == "__main__":
    main()
