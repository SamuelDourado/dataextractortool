from argparse import Namespace

from dataextractor.config.settings import (
    GitSettings,
    JiraSettings,
    OutputSettings,
    Settings,
)


class TestGitSettings:
    def test_default_values(self):
        git = GitSettings()

        assert git.url == ""
        assert git.version == ""
        assert git.type == ""
        assert git.token == ""
        assert not git.projects


class TestJiraSettings:
    def test_default_values(self):
        jira = JiraSettings()

        assert jira.url == ""
        assert jira.version == ""
        assert jira.token == ""


class TestOutputSettings:
    def test_default_values(self):
        outputs = OutputSettings()

        assert outputs.type == ""
        assert outputs.db_url == ""
        assert outputs.git_table_name == ""
        assert outputs.jira_table_name == ""
        assert outputs.logs_git_table_name == ""
        assert outputs.logs_jira_table_name == ""


class TestSettings:
    def test_load_from_yaml_file(self, tmp_path):
        config_content = """
inputs:
  git_url: https://gitlab.example.com
  git_version: "15.0"
  git_type: gitlab
  git_token: secret-token
  git_projects:
    - project1
    - project2
  jira_url: https://jira.example.com
  jira_version: "9.0"
  jira_token: jira-secret

outputs:
  type: postgres
  db_url: postgresql://localhost/db
  git_table_name: git_data
  jira_table_name: jira_data
  logs_git_table_name: git_logs
  logs_jira_table_name: jira_logs
"""
        config_file = tmp_path / "test_settings.yaml"
        config_file.write_text(config_content)

        settings = Settings.load(config_file)

        assert settings.git.url == "https://gitlab.example.com"
        assert settings.git.version == "15.0"
        assert settings.git.type == "gitlab"
        assert settings.git.token == "secret-token"
        assert settings.git.projects == ["project1", "project2"]
        assert settings.jira.url == "https://jira.example.com"
        assert settings.jira.version == "9.0"
        assert settings.jira.token == "jira-secret"
        assert settings.outputs.type == "postgres"
        assert settings.outputs.db_url == "postgresql://localhost/db"
        assert settings.outputs.git_table_name == "git_data"
        assert settings.outputs.jira_table_name == "jira_data"
        assert settings.outputs.logs_git_table_name == "git_logs"
        assert settings.outputs.logs_jira_table_name == "jira_logs"

    def test_default_factory_creates_empty_settings(self):
        settings = Settings()

        assert settings.git.url == ""
        assert settings.jira.url == ""
        assert settings.outputs.type == ""


class TestSettingsCliOverrides:
    def _create_config_file(self, tmp_path):
        config_content = """
inputs:
  git_url: https://original-gitlab.com
  git_version: "14.0"
  git_type: gitlab
  git_token: original-token
  git_projects:
    - original-project
  jira_url: https://original-jira.com
  jira_version: "8.0"
  jira_token: original-jira-token

outputs:
  type: postgres
  db_url: postgresql://original/db
  git_table_name: original_git
  jira_table_name: original_jira
  logs_git_table_name: original_git_logs
  logs_jira_table_name: original_jira_logs
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)
        return config_file

    def _create_cli_args(self, **kwargs):
        defaults = {
            "g": False,
            "j": False,
            "no_env": False,
            "git_url": None,
            "git_version": None,
            "git_type": None,
            "git_token": None,
            "git_projects": None,
            "jira_url": None,
            "jira_version": None,
            "jira_token": None,
            "output_type": None,
            "db_url": None,
            "git_table_name": None,
            "jira_table_name": None,
            "logs_git_table_name": None,
            "logs_jira_table_name": None,
        }
        defaults.update(kwargs)
        return Namespace(**defaults)

    def test_cli_overrides_git_url(self, tmp_path):
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(git_url="https://cli-gitlab.com")

        settings = Settings.load(config_file, cli_args=args)

        assert settings.git.url == "https://cli-gitlab.com"

    def test_cli_overrides_git_version(self, tmp_path):
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(git_version="16.0")

        settings = Settings.load(config_file, cli_args=args)

        assert settings.git.version == "16.0"

    def test_cli_overrides_git_type(self, tmp_path):
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(git_type="github")

        settings = Settings.load(config_file, cli_args=args)

        assert settings.git.type == "github"

    def test_cli_overrides_git_token(self, tmp_path):
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(git_token="cli-token")

        settings = Settings.load(config_file, cli_args=args)

        assert settings.git.token == "cli-token"

    def test_cli_overrides_git_projects(self, tmp_path):
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(git_projects=["cli-project1", "cli-project2"])

        settings = Settings.load(config_file, cli_args=args)

        assert settings.git.projects == ["cli-project1", "cli-project2"]

    def test_cli_overrides_jira_url(self, tmp_path):
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(jira_url="https://cli-jira.com")

        settings = Settings.load(config_file, cli_args=args)

        assert settings.jira.url == "https://cli-jira.com"

    def test_cli_overrides_output_type(self, tmp_path):
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(output_type="mysql")

        settings = Settings.load(config_file, cli_args=args)

        assert settings.outputs.type == "mysql"

    def test_cli_overrides_db_url(self, tmp_path):
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(db_url="mysql://cli/db")

        settings = Settings.load(config_file, cli_args=args)

        assert settings.outputs.db_url == "mysql://cli/db"

    def test_no_overrides_when_cli_args_none(self, tmp_path):
        config_file = self._create_config_file(tmp_path)

        settings = Settings.load(config_file, cli_args=None)

        assert settings.git.url == "https://original-gitlab.com"
        assert settings.jira.url == "https://original-jira.com"
        assert settings.outputs.type == "postgres"

    def test_partial_overrides(self, tmp_path):
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(git_url="https://cli-gitlab.com", output_type="mysql")

        settings = Settings.load(config_file, cli_args=args)

        # Overridden values
        assert settings.git.url == "https://cli-gitlab.com"
        assert settings.outputs.type == "mysql"
        # Original values preserved
        assert settings.git.token == "original-token"
        assert settings.jira.url == "https://original-jira.com"
        assert settings.outputs.db_url == "postgresql://original/db"


class TestSettingsEmptyOverrides:
    """Test that empty values can override config file settings."""

    def _create_config_file(self, tmp_path):
        config_content = """
inputs:
  git_url: https://original-gitlab.com
  git_token: original-token
  git_projects:
    - project1
    - project2

outputs:
  type: postgres
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)
        return config_file

    def _create_cli_args(self, **kwargs):
        defaults = {
            "g": False,
            "j": False,
            "no_env": False,
            "git_url": None,
            "git_version": None,
            "git_type": None,
            "git_token": None,
            "git_projects": None,
            "jira_url": None,
            "jira_version": None,
            "jira_token": None,
            "output_type": None,
            "db_url": None,
            "git_table_name": None,
            "jira_table_name": None,
            "logs_git_table_name": None,
            "logs_jira_table_name": None,
        }
        defaults.update(kwargs)
        return Namespace(**defaults)

    def test_empty_list_clears_projects(self, tmp_path):
        """Empty list should override config file projects."""
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(git_projects=[])

        settings = Settings.load(config_file, cli_args=args)

        assert not settings.git.projects

    def test_empty_string_clears_token(self, tmp_path):
        """Empty string should override config file token."""
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(git_token="")

        settings = Settings.load(config_file, cli_args=args)

        assert settings.git.token == ""


class TestSettingsNoEnvFlag:
    """Test the --no-env flag behavior."""

    def _create_config_file(self, tmp_path):
        config_content = """
inputs:
  git_url: https://env-gitlab.com
  git_token: env-token

outputs:
  type: postgres
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)
        return config_file

    def _create_cli_args(self, **kwargs):
        defaults = {
            "g": False,
            "j": False,
            "no_env": False,
            "git_url": None,
            "git_version": None,
            "git_type": None,
            "git_token": None,
            "git_projects": None,
            "jira_url": None,
            "jira_version": None,
            "jira_token": None,
            "output_type": None,
            "db_url": None,
            "git_table_name": None,
            "jira_table_name": None,
            "logs_git_table_name": None,
            "logs_jira_table_name": None,
        }
        defaults.update(kwargs)
        return Namespace(**defaults)

    def test_no_env_ignores_config_file(self, tmp_path):
        """With --no-env, config file should be ignored."""
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(no_env=True)

        settings = Settings.load(config_file, cli_args=args)

        # Should have empty defaults, not values from config
        assert settings.git.url == ""
        assert settings.git.token == ""
        assert settings.outputs.type == ""

    def test_no_env_with_cli_args(self, tmp_path):
        """With --no-env, only CLI args should be used."""
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(
            no_env=True,
            git_url="https://cli-gitlab.com",
            git_token="cli-token"
        )

        settings = Settings.load(config_file, cli_args=args)

        assert settings.git.url == "https://cli-gitlab.com"
        assert settings.git.token == "cli-token"
        # Other fields should be empty
        assert settings.outputs.type == ""

    def test_without_no_env_uses_config_file(self, tmp_path):
        """Without --no-env, config file should be used."""
        config_file = self._create_config_file(tmp_path)
        args = self._create_cli_args(no_env=False)

        settings = Settings.load(config_file, cli_args=args)

        assert settings.git.url == "https://env-gitlab.com"
        assert settings.git.token == "env-token"
        assert settings.outputs.type == "postgres"
