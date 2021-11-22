from typing import List

from .project import Project
from ..representers import ReposRepresenter


# View object for colelction of Github projects
class AllProjects:
    def __init__(self, all_repos: ReposRepresenter):
        self._all_repos = all_repos

    @property
    def none(self) -> bool:
        return len(self._all_repos.repos) == 0

    @property
    def any(self) -> bool:
        return len(self._all_repos.repos) > 0

    @property
    def collection(self) -> List[Project]:
        return list(map(lambda repo: Project(repo), self._all_repos.repos))
