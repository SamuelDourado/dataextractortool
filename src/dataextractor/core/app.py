import gitlab

GITLAB_URL = "https://git.universal.org.br"          # e.g., "https://gitlab.mycorp.local"
TOKEN      =  "1fBS9nigzEQsSUPYisRM"             # create a PAT with 'api' scope in 12.3.2
MAX_WORKERS = 4

def get_projects():
    gl = gitlab.Gitlab(GITLAB_URL, private_token=TOKEN)
    gl.auth()
    # list all the projects
    projects = gl.projects.list(iterator=True)
    p = []
    for project in projects:
        # print(project.id, project.path_with_namespace, project.http_url_to_repo)
        p.append(project.http_url_to_repo)
    return p

def main():
    repos = get_projects()
    print(f"Total repositories: {len(repos)}")
    for repo in repos:
        print(repo)

if __name__ == "__main__":
    main()
