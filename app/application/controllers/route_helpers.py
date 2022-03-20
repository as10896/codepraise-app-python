# Message Flashing helpers for FastAPI

# Refs:
# https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/
# https://github.com/pallets/flask/blob/7620cb70dbcbf71bca651e6f2eef3cbb05999272/src/flask/helpers.py#L365
# https://stackoverflow.com/questions/68681125/in-fastapi-web-application-how-to-temporarily-show-users-a-message-when-somethin

from typing import Any, List, Tuple

from fastapi import Request


def flash(request: Request, message: str, category: str = "message") -> None:
    request.session.setdefault("_flashes", []).append((category, message))


def get_flashed_messages(request: Request) -> List[Tuple[str, str]]:
    return request.session.pop("_flashes") if "_flashes" in request.session else []


def url_for(request: Request, name: str, **path_params: Any) -> str:
    """
    The default `url_for` function from Starlette would make HTTPS hosted pages request stylesheets with HTTP schemes,
    which will be blocked since the content must be served over HTTPS as well.
    Remove the URI scheme (i.e. use "//" instead of "http://" or "https://") to solve this unexpected situation.

    Refs:
    https://github.com/encode/starlette/blob/2b54f427613ebd1a6ccb2031aa97364e2d5070a5/starlette/templating.py#L68
    https://stackoverflow.com/questions/28134098/this-request-has-been-blocked-the-content-must-be-served-over-https
    """

    http_url: str = request.url_for(name, **path_params)

    return http_url.replace("http:", "")
