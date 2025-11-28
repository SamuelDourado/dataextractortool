from argparse import Namespace
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
    def load(cls, config_path: str | Path | None = None, cli_args: Namespace | None = None) -> "Settings":
        # Check if we should skip loading from env file
        use_env = True
        if cli_args and getattr(cli_args, "no_env", False):
            use_env = False

        if use_env:
            try:
                env_config = EnvConfig.load(config_path)
                settings = cls(
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
            except FileNotFoundError:
                # If env file doesn't exist, start with empty settings
                settings = cls()
        else:
            settings = cls()

        if cli_args:
            settings._apply_cli_overrides(cli_args)

        return settings

    def _apply_cli_overrides(self, args: Namespace):
        self._apply_git_overrides(args)
        self._apply_jira_overrides(args)
        self._apply_output_overrides(args)

    def _apply_git_overrides(self, args: Namespace):
        if getattr(args, "git_url", None) is not None:
            self.git.url = args.git_url
        if getattr(args, "git_version", None) is not None:
            self.git.version = args.git_version
        if getattr(args, "git_type", None) is not None:
            self.git.type = args.git_type
        if getattr(args, "git_token", None) is not None:
            self.git.token = args.git_token
        if getattr(args, "git_projects", None) is not None:
            self.git.projects = args.git_projects

    def _apply_jira_overrides(self, args: Namespace):
        if getattr(args, "jira_url", None) is not None:
            self.jira.url = args.jira_url
        if getattr(args, "jira_version", None) is not None:
            self.jira.version = args.jira_version
        if getattr(args, "jira_token", None) is not None:
            self.jira.token = args.jira_token

    def _apply_output_overrides(self, args: Namespace):
        if getattr(args, "output_type", None) is not None:
            self.outputs.type = args.output_type
        if getattr(args, "db_url", None) is not None:
            self.outputs.db_url = args.db_url
        if getattr(args, "git_table_name", None) is not None:
            self.outputs.git_table_name = args.git_table_name
        if getattr(args, "jira_table_name", None) is not None:
            self.outputs.jira_table_name = args.jira_table_name
        if getattr(args, "logs_git_table_name", None) is not None:
            self.outputs.logs_git_table_name = args.logs_git_table_name
        if getattr(args, "logs_jira_table_name", None) is not None:
            self.outputs.logs_jira_table_name = args.logs_jira_table_name
