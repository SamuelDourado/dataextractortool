import argparse


class CliHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Data Extractor CLI"
        )
        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        # Source selection (mutually exclusive)
        group = self.parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "-g",
            action="store_true",
            help="Extract data from Git"
        )
        group.add_argument(
            "-j",
            action="store_true",
            help="Extract data from Jira"
        )

        # Configuration options
        config_group = self.parser.add_argument_group("Configuration Options")
        config_group.add_argument(
            "--no-env",
            action="store_true",
            help="Ignore .env.yaml file and use only CLI arguments"
        )

        # Git input parameters
        git_group = self.parser.add_argument_group("Git Options")
        git_group.add_argument(
            "--git-url",
            type=str,
            help="Git server URL"
        )
        git_group.add_argument(
            "--git-version",
            type=str,
            help="Git server version"
        )
        git_group.add_argument(
            "--git-type",
            type=str,
            choices=["gitlab", "github", "bitbucket"],
            help="Git server type"
        )
        git_group.add_argument(
            "--git-token",
            type=str,
            help="Git authentication token"
        )
        git_group.add_argument(
            "--git-projects",
            type=str,
            nargs="*",
            help="List of Git project URLs"
        )

        # Jira input parameters
        jira_group = self.parser.add_argument_group("Jira Options")
        jira_group.add_argument(
            "--jira-url",
            type=str,
            help="Jira server URL"
        )
        jira_group.add_argument(
            "--jira-version",
            type=str,
            help="Jira server version"
        )
        jira_group.add_argument(
            "--jira-token",
            type=str,
            help="Jira authentication token"
        )

        # Output parameters
        output_group = self.parser.add_argument_group("Output Options")
        output_group.add_argument(
            "--output-type",
            type=str,
            help="Output type (e.g., postgres, mysql)"
        )
        output_group.add_argument(
            "--db-url",
            type=str,
            help="Database connection URL"
        )
        output_group.add_argument(
            "--git-table-name",
            type=str,
            help="Table name for Git data"
        )
        output_group.add_argument(
            "--jira-table-name",
            type=str,
            help="Table name for Jira data"
        )
        output_group.add_argument(
            "--logs-git-table-name",
            type=str,
            help="Table name for Git logs"
        )
        output_group.add_argument(
            "--logs-jira-table-name",
            type=str,
            help="Table name for Jira logs"
        )

    def parse(self, args=None):
        self.args = self.parser.parse_args(args)
        return self.args
