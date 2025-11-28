import pytest

from dataextractor.cli import CliHandler


class TestCliHandler:
    def test_parse_git_flag(self):
        cli = CliHandler()
        args = cli.parse(["-g"])

        assert args.g is True
        assert args.j is False

    def test_parse_jira_flag(self):
        cli = CliHandler()
        args = cli.parse(["-j"])

        assert args.g is False
        assert args.j is True

    def test_flags_are_mutually_exclusive(self):
        cli = CliHandler()

        with pytest.raises(SystemExit):
            cli.parse(["-g", "-j"])

    def test_requires_at_least_one_flag(self):
        cli = CliHandler()

        with pytest.raises(SystemExit):
            cli.parse([])

    def test_args_stored_in_instance(self):
        cli = CliHandler()
        cli.parse(["-g"])

        assert cli.args is not None
        assert cli.args.g is True

    def test_no_env_flag_default(self):
        cli = CliHandler()
        args = cli.parse(["-g"])

        assert args.no_env is False

    def test_no_env_flag_enabled(self):
        cli = CliHandler()
        args = cli.parse(["-g", "--no-env"])

        assert args.no_env is True


class TestCliHandlerGitOptions:
    def test_parse_git_url(self):
        cli = CliHandler()
        args = cli.parse(["-g", "--git-url", "https://gitlab.example.com"])

        assert args.git_url == "https://gitlab.example.com"

    def test_parse_git_version(self):
        cli = CliHandler()
        args = cli.parse(["-g", "--git-version", "15.0"])

        assert args.git_version == "15.0"

    def test_parse_git_type(self):
        cli = CliHandler()
        args = cli.parse(["-g", "--git-type", "gitlab"])

        assert args.git_type == "gitlab"

    def test_parse_git_type_choices(self):
        cli = CliHandler()

        with pytest.raises(SystemExit):
            cli.parse(["-g", "--git-type", "invalid"])

    def test_parse_git_token(self):
        cli = CliHandler()
        args = cli.parse(["-g", "--git-token", "secret-token"])

        assert args.git_token == "secret-token"

    def test_parse_git_projects(self):
        cli = CliHandler()
        args = cli.parse(["-g", "--git-projects", "project1", "project2"])

        assert args.git_projects == ["project1", "project2"]


class TestCliHandlerJiraOptions:
    def test_parse_jira_url(self):
        cli = CliHandler()
        args = cli.parse(["-j", "--jira-url", "https://jira.example.com"])

        assert args.jira_url == "https://jira.example.com"

    def test_parse_jira_version(self):
        cli = CliHandler()
        args = cli.parse(["-j", "--jira-version", "9.0"])

        assert args.jira_version == "9.0"

    def test_parse_jira_token(self):
        cli = CliHandler()
        args = cli.parse(["-j", "--jira-token", "jira-secret"])

        assert args.jira_token == "jira-secret"


class TestCliHandlerOutputOptions:
    def test_parse_output_type(self):
        cli = CliHandler()
        args = cli.parse(["-g", "--output-type", "postgres"])

        assert args.output_type == "postgres"

    def test_parse_db_url(self):
        cli = CliHandler()
        args = cli.parse(["-g", "--db-url", "postgresql://localhost/db"])

        assert args.db_url == "postgresql://localhost/db"

    def test_parse_git_table_name(self):
        cli = CliHandler()
        args = cli.parse(["-g", "--git-table-name", "git_data"])

        assert args.git_table_name == "git_data"

    def test_parse_jira_table_name(self):
        cli = CliHandler()
        args = cli.parse(["-j", "--jira-table-name", "jira_data"])

        assert args.jira_table_name == "jira_data"

    def test_parse_logs_git_table_name(self):
        cli = CliHandler()
        args = cli.parse(["-g", "--logs-git-table-name", "git_logs"])

        assert args.logs_git_table_name == "git_logs"

    def test_parse_logs_jira_table_name(self):
        cli = CliHandler()
        args = cli.parse(["-j", "--logs-jira-table-name", "jira_logs"])

        assert args.logs_jira_table_name == "jira_logs"


class TestCliHandlerAllOptions:
    def test_parse_all_git_options(self):
        cli = CliHandler()
        args = cli.parse([
            "-g",
            "--git-url", "https://gitlab.example.com",
            "--git-version", "15.0",
            "--git-type", "gitlab",
            "--git-token", "secret",
            "--git-projects", "proj1", "proj2",
            "--output-type", "postgres",
            "--db-url", "postgresql://localhost/db",
            "--git-table-name", "git_data",
            "--logs-git-table-name", "git_logs",
        ])

        assert args.g is True
        assert args.git_url == "https://gitlab.example.com"
        assert args.git_version == "15.0"
        assert args.git_type == "gitlab"
        assert args.git_token == "secret"
        assert args.git_projects == ["proj1", "proj2"]
        assert args.output_type == "postgres"
        assert args.db_url == "postgresql://localhost/db"
        assert args.git_table_name == "git_data"
        assert args.logs_git_table_name == "git_logs"

    def test_parse_all_jira_options(self):
        cli = CliHandler()
        args = cli.parse([
            "-j",
            "--jira-url", "https://jira.example.com",
            "--jira-version", "9.0",
            "--jira-token", "jira-secret",
            "--output-type", "mysql",
            "--db-url", "mysql://localhost/db",
            "--jira-table-name", "jira_data",
            "--logs-jira-table-name", "jira_logs",
        ])

        assert args.j is True
        assert args.jira_url == "https://jira.example.com"
        assert args.jira_version == "9.0"
        assert args.jira_token == "jira-secret"
        assert args.output_type == "mysql"
        assert args.db_url == "mysql://localhost/db"
        assert args.jira_table_name == "jira_data"
        assert args.logs_jira_table_name == "jira_logs"
