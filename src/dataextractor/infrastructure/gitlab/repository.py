import gitlab

from dataextractor.config import Settings
from dataextractor.core.entities import ProjectInfo
from dataextractor.core.interfaces import ProjectRepository


class GitLabProjectRepository(ProjectRepository):
    def __init__(self, settings: Settings):
        self.settings = settings
        self._client: gitlab.Gitlab | None = None

    @property
    def client(self) -> gitlab.Gitlab:
        if self._client is None:
            self._client = gitlab.Gitlab(
                self.settings.gitlab.url,
                private_token=self.settings.gitlab.token,
            )
            self._client.auth()
        return self._client

    def get_all_projects(self) -> list[ProjectInfo]:
        projects = self.client.projects.list(iterator=True)
        return [self._to_project_info(p) for p in projects]

    def _to_project_info(self, project) -> ProjectInfo:
        return ProjectInfo(
            id=project.id,
            name=project.name,
            path_with_namespace=project.path_with_namespace,
            http_url=project.http_url_to_repo,
            access_level=self._get_access_level(project),
        )

    def _get_access_level(self, project) -> int | None:
        permissions = project.permissions
        if permissions.get("project_access"):
            return permissions["project_access"]["access_level"]
        if permissions.get("group_access"):
            return permissions["group_access"]["access_level"]
        return None
