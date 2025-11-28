import pytest

from dataextractor.config.env import (
    EnvConfig,
    GitInputs,
    Inputs,
    JiraInputs,
    Outputs,
)


class TestGitInputs:
    def test_default_values(self):
        git = GitInputs()

        assert git.git_url == ""
        assert git.git_version == ""
        assert git.git_type == ""
        assert git.git_token == ""
        assert not git.git_projects


class TestJiraInputs:
    def test_default_values(self):
        jira = JiraInputs()

        assert jira.jira_url == ""
        assert jira.jira_version == ""
        assert jira.jira_token == ""


class TestInputs:
    def test_from_dict_with_full_data(self):
        data = {
            "git_url": "https://gitlab.com",
            "git_version": "15.0",
            "git_type": "gitlab",
            "git_token": "secret-token",
            "git_projects": ["project1", "project2"],
            "jira_url": "https://jira.com",
            "jira_version": "9.0",
            "jira_token": "jira-token",
        }

        inputs = Inputs.from_dict(data)

        assert inputs.git.git_url == "https://gitlab.com"
        assert inputs.git.git_version == "15.0"
        assert inputs.git.git_type == "gitlab"
        assert inputs.git.git_token == "secret-token"
        assert inputs.git.git_projects == ["project1", "project2"]
        assert inputs.jira.jira_url == "https://jira.com"
        assert inputs.jira.jira_version == "9.0"
        assert inputs.jira.jira_token == "jira-token"

    def test_from_dict_with_empty_data(self):
        inputs = Inputs.from_dict({})

        assert inputs.git.git_url == ""
        assert not inputs.git.git_projects
        assert inputs.jira.jira_url == ""

    def test_from_dict_handles_none_values(self):
        data = {
            "git_url": None,
            "git_version": None,
            "git_projects": None,
        }

        inputs = Inputs.from_dict(data)

        assert inputs.git.git_url == ""
        assert inputs.git.git_version == ""
        assert not inputs.git.git_projects


class TestOutputs:
    def test_from_dict_with_full_data(self):
        data = {
            "type": "postgres",
            "db_url": "postgresql://localhost/db",
            "git_table_name": "git_data",
            "jira_table_name": "jira_data",
            "logs_git_table_name": "git_logs",
            "logs_jira_table_name": "jira_logs",
        }

        outputs = Outputs.from_dict(data)

        assert outputs.type == "postgres"
        assert outputs.db_url == "postgresql://localhost/db"
        assert outputs.git_table_name == "git_data"
        assert outputs.jira_table_name == "jira_data"
        assert outputs.logs_git_table_name == "git_logs"
        assert outputs.logs_jira_table_name == "jira_logs"

    def test_from_dict_with_empty_data(self):
        outputs = Outputs.from_dict({})

        assert outputs.type == ""
        assert outputs.db_url == ""


class TestEnvConfig:
    def test_load_from_yaml_file(self, tmp_path):
        config_content = """
inputs:
  git_url: https://gitlab.example.com
  git_type: gitlab
  git_token: my-token
  git_projects:
    - project1
    - project2

outputs:
  type: postgres
  db_url: postgresql://localhost/test
"""
        config_file = tmp_path / "test_config.yaml"
        config_file.write_text(config_content)

        config = EnvConfig.load(config_file)

        assert config.inputs.git.git_url == "https://gitlab.example.com"
        assert config.inputs.git.git_type == "gitlab"
        assert config.inputs.git.git_token == "my-token"
        assert config.inputs.git.git_projects == ["project1", "project2"]
        assert config.outputs.type == "postgres"
        assert config.outputs.db_url == "postgresql://localhost/test"

    def test_load_raises_file_not_found(self, tmp_path):
        non_existent = tmp_path / "non_existent.yaml"

        with pytest.raises(FileNotFoundError) as exc_info:
            EnvConfig.load(non_existent)

        assert "Config file not found" in str(exc_info.value)

    def test_load_handles_empty_yaml(self, tmp_path):
        config_file = tmp_path / "empty.yaml"
        config_file.write_text("")

        config = EnvConfig.load(config_file)

        assert config.inputs.git.git_url == ""
        assert config.outputs.type == ""

    def test_default_config_name(self):
        assert EnvConfig.DEFAULT_CONFIG_NAME == ".env.yaml"
