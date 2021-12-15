from functools import total_ordering
from itertools import chain, starmap
from typing import Dict, Iterable, List, Set

from typing_helpers import Contribution, ContributorEmail

from ..representers import FolderSummaryRepresenter


class ContributorView:
    def __init__(self, email: str, contribution: Contribution):
        self._email = email
        self._name = contribution["name"]

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.email == other.email

    def __hash__(self) -> int:
        return hash("".join([self.name, self.email]))


class ContributionView:
    def __init__(self, email: str, contribution: Contribution):
        self._contributor = ContributorView(email, contribution)
        self._count = contribution["count"]

    @property
    def contributor(self) -> ContributorView:
        return self._contributor

    @property
    def count(self) -> int:
        return self._count


@total_ordering
class AssetContribution:
    def __init__(
        self,
        name: str,
        contributions: Dict[ContributorEmail, Contribution],
        base_path: str,
    ):
        self._base_path = base_path
        self._name = name

        self._contributions = {}
        for email, contribution in contributions.items():
            c_view = ContributionView(email, contribution)
            self._contributions[c_view.contributor] = c_view.count

    @property
    def name(self) -> str:
        return self._name

    @property
    def base_path(self) -> str:
        return self._base_path

    @property
    def contributions(self) -> Dict[ContributorView, int]:
        return self._contributions

    @property
    def link(self) -> str:
        return ""

    def __lt__(self, other) -> bool:
        return self.name < other.name

    def __eq__(self, other) -> bool:
        return self.name == other.name


class SubfolderContribution(AssetContribution):
    @property
    def link(self) -> str:
        return "/".join([self.base_path, self.name])


class FolderSummaryView:
    def __init__(self, summary: FolderSummaryRepresenter, request_path: str):
        self._summary = summary
        self._request_path = request_path

    @property
    def name(self) -> str:
        return self._summary.folder_name

    @property
    def base_folder(self) -> SubfolderContribution:
        return self.all_folders[0]

    @property
    def subfolders(self) -> List[SubfolderContribution]:
        return self.all_folders[1:]  # remove blank base folder

    @property
    def base_files(self) -> List[AssetContribution]:
        return list(
            starmap(
                lambda filename, contributions: AssetContribution(
                    filename, contributions, self._request_path
                ),
                self._summary.base_files.items(),
            )
        )

    @property
    def contributors(self) -> Set[ContributorView]:
        if not hasattr(self, "_contributors"):
            # use "|" to union two sets
            self._contributors = self._uniq_contributors(
                self._summary.subfolders
            ) | self._uniq_contributors(self._summary.base_files)
        return self._contributors

    def _uniq_contributors(
        self, asset_summary: Dict[str, Dict[ContributorEmail, Contribution]]
    ) -> Set[ContributorView]:
        contributors: Iterable[Iterable[ContributorView]] = map(
            lambda contributions: starmap(
                lambda email, contribution: ContributorView(email, contribution),
                contributions.items(),
            ),
            asset_summary.values(),
        )
        return set(chain.from_iterable(contributors))

    @property
    def all_folders(self) -> List[SubfolderContribution]:
        if not hasattr(self, "_all_folders"):
            self._all_folders = sorted(
                starmap(
                    lambda subfolder, contributions: SubfolderContribution(
                        subfolder, contributions, self._request_path
                    ),
                    self._summary.subfolders.items(),
                )
            )
        return self._all_folders
