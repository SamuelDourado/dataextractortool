from dataclasses import dataclass

@dataclass
class ProjectInfo:
    id: int
    name: str
    path_with_namespace: str
    http_url: str
    access_level: int | None = None

    @property
    def access_level_name(self) -> str:
        access_names = {
            10: "Guest",
            20: "Reporter",
            30: "Developer",
            40: "Maintainer",
            50: "Owner",
        }
        if self.access_level is None:
            return "None"
        return access_names.get(self.access_level, f"Unknown ({self.access_level})")
