from dataclasses import dataclass, field
from pathlib import Path

from dataextractor.config.env import EnvConfig


@dataclass
class GitSettings:
    url: str = ""
    version: str = ""
    type: str = ""
    token: str = ""
    projects: list[str] = field(default_factory=list)


@dataclass
class JiraSettings:
    url: str = ""
    version: str = ""
    token: str = ""


# pylint: disable=duplicate-code
@dataclass
class OutputSettings:
    type: str = ""
    db_url: str = ""
    git_table_name: str = ""
    jira_table_name: str = ""
    logs_git_table_name: str = ""
    logs_jira_table_name: str = ""
# pylint: enable=duplicate-code


@dataclass
class Settings:
    git: GitSettings = field(default_factory=GitSettings)
    jira: JiraSettings = field(default_factory=JiraSettings)
    outputs: OutputSettings = field(default_factory=OutputSettings)

    @classmethod
    def load(cls, config_path: str | Path | None = None) -> "Settings":
        env_config = EnvConfig.load(config_path)

        return cls(
            git=GitSettings(
                url=env_config.inputs.git.git_url,
                version=env_config.inputs.git.git_version,
                type=env_config.inputs.git.git_type,
                token=env_config.inputs.git.git_token,
                projects=env_config.inputs.git.git_projects,
            ),
            jira=JiraSettings(
                url=env_config.inputs.jira.jira_url,
                version=env_config.inputs.jira.jira_version,
                token=env_config.inputs.jira.jira_token,
            ),
            outputs=OutputSettings(
                type=env_config.outputs.type,
                db_url=env_config.outputs.db_url,
                git_table_name=env_config.outputs.git_table_name,
                jira_table_name=env_config.outputs.jira_table_name,
                logs_git_table_name=env_config.outputs.logs_git_table_name,
                logs_jira_table_name=env_config.outputs.logs_jira_table_name,
            ),
        )
