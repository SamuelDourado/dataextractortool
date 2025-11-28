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
