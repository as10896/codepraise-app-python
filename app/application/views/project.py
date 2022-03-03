from operator import attrgetter

from ..representers import RepoRepresenter


# View object for a single repo's Github project
class Project:
    def __init__(self, repo: RepoRepresenter):
        self._repo = repo

    @property
    def owner(self) -> str:
        return self._repo.owner.username

    @property
    def name(self) -> str:
        return self._repo.name

    @property
    def link_to_repo(self) -> str:
        return f"/repo/{self.owner}/{self.name}"

    @property
    def github_href(self) -> str:
        if not hasattr(self, "_github_href"):
            self._github_href = f"https://github.com/{self.owner}/{self.name}"
        return self._github_href

    @property
    def contributors(self) -> str:
        return ", ".join(map(attrgetter("username"), self._repo.contributors))
