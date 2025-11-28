from dataextractor.core.entities import ProjectInfo
from dataextractor.core.interfaces import ProjectRepository
from dataextractor.core.use_cases import ListProjectsUseCase


class MockProjectRepository(ProjectRepository):
    def __init__(self, projects: list[ProjectInfo]):
        self._projects = projects

    def get_all_projects(self) -> list[ProjectInfo]:
        return self._projects


class TestListProjectsUseCase:
    def test_execute_returns_projects_from_repository(self):
        projects = [
            ProjectInfo(
                id=1,
                name="project-1",
                path_with_namespace="group/project-1",
                http_url="https://gitlab.com/group/project-1.git",
                access_level=30,
            ),
            ProjectInfo(
                id=2,
                name="project-2",
                path_with_namespace="group/project-2",
                http_url="https://gitlab.com/group/project-2.git",
                access_level=40,
            ),
        ]
        repository = MockProjectRepository(projects)
        use_case = ListProjectsUseCase(repository)

        result = use_case.execute()

        assert result == projects
        assert len(result) == 2

    def test_execute_returns_empty_list_when_no_projects(self):
        repository = MockProjectRepository([])
        use_case = ListProjectsUseCase(repository)

        result = use_case.execute()

        assert not result
        assert len(result) == 0

    def test_use_case_stores_repository(self):
        repository = MockProjectRepository([])
        use_case = ListProjectsUseCase(repository)

        assert use_case.repository is repository
