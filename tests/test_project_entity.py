import pytest

from dataextractor.core.entities import ProjectInfo


class TestProjectInfo:
    def test_create_project_info(self):
        project = ProjectInfo(
            id=1,
            name="test-project",
            path_with_namespace="group/test-project",
            http_url="https://gitlab.com/group/test-project.git",
            access_level=30,
        )

        assert project.id == 1
        assert project.name == "test-project"
        assert project.path_with_namespace == "group/test-project"
        assert project.http_url == "https://gitlab.com/group/test-project.git"
        assert project.access_level == 30

    def test_access_level_defaults_to_none(self):
        project = ProjectInfo(
            id=1,
            name="test",
            path_with_namespace="group/test",
            http_url="https://gitlab.com/group/test.git",
        )

        assert project.access_level is None

    @pytest.mark.parametrize(
        "access_level,expected_name",
        [
            (10, "Guest"),
            (20, "Reporter"),
            (30, "Developer"),
            (40, "Maintainer"),
            (50, "Owner"),
        ],
    )
    def test_access_level_name_known_levels(self, access_level, expected_name):
        project = ProjectInfo(
            id=1,
            name="test",
            path_with_namespace="group/test",
            http_url="https://gitlab.com/group/test.git",
            access_level=access_level,
        )

        assert project.access_level_name == expected_name

    def test_access_level_name_none(self):
        project = ProjectInfo(
            id=1,
            name="test",
            path_with_namespace="group/test",
            http_url="https://gitlab.com/group/test.git",
            access_level=None,
        )

        assert project.access_level_name == "None"

    def test_access_level_name_unknown(self):
        project = ProjectInfo(
            id=1,
            name="test",
            path_with_namespace="group/test",
            http_url="https://gitlab.com/group/test.git",
            access_level=99,
        )

        assert project.access_level_name == "Unknown (99)"
