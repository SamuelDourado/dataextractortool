# Enable Windows certificate store for SSL (import automatically patches certifi)
try:
    import certifi_win32  # noqa: F401  pylint: disable=unused-import
except ImportError:
    pass  # Not on Windows or package not installed

from dataextractor.cli import CliHandler
from dataextractor.config import Settings
from dataextractor.core.use_cases import ListProjectsUseCase
from dataextractor.infrastructure.gitlab import GitLabProjectRepository


def main():
    cli = CliHandler()
    args = cli.parse()

    settings = Settings.load(cli_args=args)

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
