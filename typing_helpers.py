from typing import TypedDict, TypeVar

Filename = TypeVar("Filename", bound=str)
SubfolderName = TypeVar("SubfolderName", bound=str)
SubfolderLink = TypeVar("SubfolderLink", bound=str)
ContributorEmail = TypeVar("ContributorEmail", bound=str)

Contribution = TypedDict("Contribution", {"name": str, "count": int})
ListedRepo = TypedDict(
    "ListedRepo", {"owner": str, "name": str, "gh_url": str, "num_contributors": int}
)
