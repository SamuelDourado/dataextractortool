from __future__ import annotations

import gitlab
from gitlab.v4.objects import Project

GITLAB_URL = "https://git.universal.org.br"          # e.g., "https://gitlab.mycorp.local"
TOKEN      =  "1fBS9nigzEQsSUPYisRM"             # create a PAT with 'api' scope in 12.3.2
MAX_WORKERS = 4

ACCESS_LEVEL_NAMES = {
    gitlab.const.AccessLevel.GUEST: "Guest",
    gitlab.const.AccessLevel.REPORTER: "Reporter",
    gitlab.const.AccessLevel.DEVELOPER: "Developer",
    gitlab.const.AccessLevel.MAINTAINER: "Maintainer",
    gitlab.const.AccessLevel.OWNER: "Owner",
}

def get_access_level_name(level: int | None) -> str:
    if level is None:
        return "None"
    return ACCESS_LEVEL_NAMES.get(level, f"Unknown ({level})")

def get_projects():
    gl = gitlab.Gitlab(GITLAB_URL, private_token=TOKEN)
    gl.auth()
    # list all the projects
    projects = gl.projects.list(iterator=True)
    p = []
    for project in projects:
        # print(project.id, project.path_with_namespace, project.http_url_to_repo)
        p.append(project)
    return p

def get_access_level(project: Project):
    permissions = project.permissions
    if permissions.get("project_access"):
        return permissions["project_access"]["access_level"]
    if permissions.get("group_access"):
        return permissions["group_access"]["access_level"]
    return None

def has_developer_access_level(project: Project):
    access_level = get_access_level(project)
    return access_level is not None and access_level >= gitlab.const.DEVELOPER_ACCESS

def main():
    repos = get_projects()
    print(f"Total repositories: {len(repos)}")
    for repo in repos:
        access_level = get_access_level(repo)
        print(f"Project: {repo.path_with_namespace} Access Level: {get_access_level_name(access_level)}")

if __name__ == "__main__":
    main()
