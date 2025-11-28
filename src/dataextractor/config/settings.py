import os
from dataclasses import dataclass


@dataclass
class GitLabSettings:
    url: str = "https://git.universal.org.br"
    token: str = "1fBS9nigzEQsSUPYisRM"


@dataclass
class JiraSettings:
    url: str = ""
    username: str = ""
    api_token: str = ""


@dataclass
class Settings:
    gitlab: GitLabSettings
    jira: JiraSettings

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            gitlab=GitLabSettings(
                url=os.getenv("GITLAB_URL", "https://git.universal.org.br"),
                token=os.getenv("GITLAB_TOKEN", "1fBS9nigzEQsSUPYisRM"),
            ),
            jira=JiraSettings(
                url=os.getenv("JIRA_URL", ""),
                username=os.getenv("JIRA_USERNAME", ""),
                api_token=os.getenv("JIRA_API_TOKEN", ""),
            ),
        )
