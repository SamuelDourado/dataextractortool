from dataextractor.core.entities import ProjectInfo
from dataextractor.core.interfaces import ProjectRepository


class ListProjectsUseCase:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def execute(self) -> list[ProjectInfo]:
        return self.repository.get_all_projects()
