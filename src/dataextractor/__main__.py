from dataextractor.cli import CliHandler
from dataextractor.config import Settings
from dataextractor.core.use_cases import ListProjectsUseCase
from dataextractor.infrastructure.gitlab import GitLabProjectRepository


def main():
    cli = CliHandler()
    args = cli.parse()

    settings = Settings.load()

    if args.g:
        print("git")
        repository = GitLabProjectRepository(settings)
        use_case = ListProjectsUseCase(repository)
        projects = use_case.execute()

        print(f"Total repositories: {len(projects)}")
        for project in projects:
            print(f"Project: {project.path_with_namespace} Access Level: {project.access_level_name}")

    elif args.j:
        print("jira")
        print("Jira integration not yet implemented")


if __name__ == "__main__":
    main()
