# Data Extractor

A CLI tool for extracting project data from Git (GitLab, GitHub, Bitbucket) and Jira, built with Clean Architecture principles.

## Requirements

- Python 3.12+
- Poetry

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd dataextractor

# Install dependencies
poetry install
```

## Configuration

Create a `.env.yaml` file in the project root:

```yaml
inputs:
  git_url: https://gitlab.example.com
  git_version: "15.0"
  git_type: gitlab
  git_token: your-git-token
  git_projects:
    - project-url-1
    - project-url-2

  jira_url: https://jira.example.com
  jira_version: "9.0"
  jira_token: your-jira-token

outputs:
  type: postgres
  db_url: postgresql://localhost/dataextractor
  git_table_name: git_data
  jira_table_name: jira_data
  logs_git_table_name: git_logs
  logs_jira_table_name: jira_logs
```

## Usage

### Extract Git Data

```bash
# Using config file
poetry run dataextractor -g

# Override config with CLI arguments
poetry run dataextractor -g --git-url https://gitlab.com --git-token your-token

# Use only CLI arguments (ignore .env.yaml)
poetry run dataextractor -g --no-env --git-url https://gitlab.com --git-token your-token
```

### Extract Jira Data

```bash
# Using config file
poetry run dataextractor -j

# Override config with CLI arguments
poetry run dataextractor -j --jira-url https://jira.example.com --jira-token your-token
```

### CLI Options

| Option | Description |
|--------|-------------|
| `-g` | Extract data from Git |
| `-j` | Extract data from Jira |
| `--no-env` | Ignore .env.yaml file |
| `--git-url` | Git server URL |
| `--git-version` | Git server version |
| `--git-type` | Git type: gitlab, github, bitbucket |
| `--git-token` | Git authentication token |
| `--git-projects` | List of project URLs |
| `--jira-url` | Jira server URL |
| `--jira-version` | Jira server version |
| `--jira-token` | Jira authentication token |
| `--output-type` | Output type (postgres, mysql) |
| `--db-url` | Database connection URL |
| `--git-table-name` | Table name for Git data |
| `--jira-table-name` | Table name for Jira data |

### Show Help

```bash
poetry run dataextractor -h
```

## Project Structure

```
src/dataextractor/
├── __main__.py              # Entry point
├── cli/                     # CLI handling
│   └── handler.py
├── config/                  # Configuration management
│   ├── env.py               # YAML config loader
│   └── settings.py          # Application settings
├── core/                    # Business logic (Clean Architecture)
│   ├── entities/            # Domain models
│   │   └── project.py
│   ├── interfaces/          # Abstract contracts (ports)
│   │   └── repository.py
│   └── use_cases/           # Application use cases
│       └── list_projects.py
└── infrastructure/          # External implementations (adapters)
    ├── gitlab/
    │   └── repository.py
    └── jira/
        └── repository.py
```

## Development

### Run Tests

```bash
poetry run pytest
```

### Run Tests with Coverage

```bash
poetry run pytest --cov=dataextractor
```

### Run Linting

```bash
poetry run pylint src/dataextractor
```

