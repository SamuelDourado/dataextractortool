from unittest.mock import MagicMock, patch

from dataextractor.config.settings import GitSettings, JiraSettings, OutputSettings, Settings
from dataextractor.core.entities import ProjectInfo
from dataextractor.infrastructure.gitlab import GitLabProjectRepository


class TestGitLabProjectRepository:
    def _create_settings(self):
        return Settings(
            git=GitSettings(
                url="https://gitlab.example.com",
                token="test-token",
            ),
            jira=JiraSettings(),
            outputs=OutputSettings(),
        )

    def test_init_stores_settings(self):
        settings = self._create_settings()

        repository = GitLabProjectRepository(settings)

        assert repository.settings is settings
        assert repository._client is None  # pylint: disable=protected-access

    @patch("dataextractor.infrastructure.gitlab.repository.gitlab.Gitlab")
    def test_client_property_creates_gitlab_instance(self, mock_gitlab_class):
        settings = self._create_settings()
        mock_client = MagicMock()
        mock_gitlab_class.return_value = mock_client
        repository = GitLabProjectRepository(settings)

        client = repository.client

        mock_gitlab_class.assert_called_once_with(
            "https://gitlab.example.com",
            private_token="test-token",
        )
        mock_client.auth.assert_called_once()
        assert client is mock_client

    @patch("dataextractor.infrastructure.gitlab.repository.gitlab.Gitlab")
    def test_client_property_caches_instance(self, mock_gitlab_class):
        settings = self._create_settings()
        mock_client = MagicMock()
        mock_gitlab_class.return_value = mock_client
        repository = GitLabProjectRepository(settings)

        client1 = repository.client
        client2 = repository.client

        assert client1 is client2
        mock_gitlab_class.assert_called_once()

    @patch("dataextractor.infrastructure.gitlab.repository.gitlab.Gitlab")
    def test_get_all_projects_returns_project_info_list(self, mock_gitlab_class):
        settings = self._create_settings()
        mock_client = MagicMock()
        mock_gitlab_class.return_value = mock_client

        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.name = "test-project"
        mock_project.path_with_namespace = "group/test-project"
        mock_project.http_url_to_repo = "https://gitlab.example.com/group/test-project.git"
        mock_project.permissions = {"project_access": {"access_level": 30}}
        mock_client.projects.list.return_value = [mock_project]

        repository = GitLabProjectRepository(settings)
        projects = repository.get_all_projects()

        assert len(projects) == 1
        assert isinstance(projects[0], ProjectInfo)
        assert projects[0].id == 1
        assert projects[0].name == "test-project"
        assert projects[0].path_with_namespace == "group/test-project"
        assert projects[0].http_url == "https://gitlab.example.com/group/test-project.git"
        assert projects[0].access_level == 30

    @patch("dataextractor.infrastructure.gitlab.repository.gitlab.Gitlab")
    def test_get_access_level_from_project_access(self, mock_gitlab_class):
        settings = self._create_settings()
        mock_client = MagicMock()
        mock_gitlab_class.return_value = mock_client

        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.name = "test"
        mock_project.path_with_namespace = "group/test"
        mock_project.http_url_to_repo = "https://gitlab.example.com/group/test.git"
        mock_project.permissions = {"project_access": {"access_level": 40}, "group_access": None}
        mock_client.projects.list.return_value = [mock_project]

        repository = GitLabProjectRepository(settings)
        projects = repository.get_all_projects()

        assert projects[0].access_level == 40

    @patch("dataextractor.infrastructure.gitlab.repository.gitlab.Gitlab")
    def test_get_access_level_from_group_access(self, mock_gitlab_class):
        settings = self._create_settings()
        mock_client = MagicMock()
        mock_gitlab_class.return_value = mock_client

        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.name = "test"
        mock_project.path_with_namespace = "group/test"
        mock_project.http_url_to_repo = "https://gitlab.example.com/group/test.git"
        mock_project.permissions = {"project_access": None, "group_access": {"access_level": 30}}
        mock_client.projects.list.return_value = [mock_project]

        repository = GitLabProjectRepository(settings)
        projects = repository.get_all_projects()

        assert projects[0].access_level == 30

    @patch("dataextractor.infrastructure.gitlab.repository.gitlab.Gitlab")
    def test_get_access_level_none_when_no_access(self, mock_gitlab_class):
        settings = self._create_settings()
        mock_client = MagicMock()
        mock_gitlab_class.return_value = mock_client

        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.name = "test"
        mock_project.path_with_namespace = "group/test"
        mock_project.http_url_to_repo = "https://gitlab.example.com/group/test.git"
        mock_project.permissions = {"project_access": None, "group_access": None}
        mock_client.projects.list.return_value = [mock_project]

        repository = GitLabProjectRepository(settings)
        projects = repository.get_all_projects()

        assert projects[0].access_level is None
