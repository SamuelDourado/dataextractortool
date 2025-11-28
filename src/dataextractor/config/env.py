from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class GitInputs:
    git_url: str = ""
    git_version: str = ""
    git_type: str = ""
    git_token: str = ""
    git_projects: list[str] = field(default_factory=list)


@dataclass
class JiraInputs:
    jira_url: str = ""
    jira_version: str = ""
    jira_token: str = ""


@dataclass
class Inputs:
    git: GitInputs = field(default_factory=GitInputs)
    jira: JiraInputs = field(default_factory=JiraInputs)

    @classmethod
    def from_dict(cls, data: dict) -> "Inputs":
        return cls(
            git=GitInputs(
                git_url=data.get("git_url", ""),
                git_version=data.get("git_version", "") or "",
                git_type=data.get("git_type", ""),
                git_token=data.get("git_token", "") or "",
                git_projects=data.get("git_projects", []) or [],
            ),
            jira=JiraInputs(
                jira_url=data.get("jira_url", "") or "",
                jira_version=data.get("jira_version", "") or "",
                jira_token=data.get("jira_token", "") or "",
            ),
        )


@dataclass
class Outputs:
    type: str = ""
    db_url: str = ""
    git_table_name: str = ""
    jira_table_name: str = ""
    logs_git_table_name: str = ""
    logs_jira_table_name: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "Outputs":
        return cls(
            type=data.get("type", "") or "",
            db_url=data.get("db_url", "") or "",
            git_table_name=data.get("git_table_name", "") or "",
            jira_table_name=data.get("jira_table_name", "") or "",
            logs_git_table_name=data.get("logs_git_table_name", "") or "",
            logs_jira_table_name=data.get("logs_jira_table_name", "") or "",
        )


@dataclass
class EnvConfig:
    inputs: Inputs = field(default_factory=Inputs)
    outputs: Outputs = field(default_factory=Outputs)

    @classmethod
    def load(cls, path: str | Path = ".env.yaml") -> "EnvConfig":
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        return cls(
            inputs=Inputs.from_dict(data.get("inputs", {})),
            outputs=Outputs.from_dict(data.get("outputs", {})),
        )
