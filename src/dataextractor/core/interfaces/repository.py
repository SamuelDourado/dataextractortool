from abc import ABC, abstractmethod

from dataextractor.core.entities import ProjectInfo


class ProjectRepository(ABC):
    @abstractmethod
    def get_all_projects(self) -> list[ProjectInfo]:
        pass
