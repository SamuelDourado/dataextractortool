from dataextractor.config import Settings
from dataextractor.core.entities import ProjectInfo
from dataextractor.core.interfaces import ProjectRepository


class JiraProjectRepository(ProjectRepository):
    """Placeholder for Jira integration - to be implemented."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def get_all_projects(self) -> list[ProjectInfo]:
        raise NotImplementedError("Jira integration not yet implemented")
