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
