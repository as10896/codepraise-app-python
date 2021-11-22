# Message Flashing helpers for FastAPI

# Refs:
# https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/
# https://github.com/pallets/flask/blob/7620cb70dbcbf71bca651e6f2eef3cbb05999272/src/flask/helpers.py#L365
# https://stackoverflow.com/questions/68681125/in-fastapi-web-application-how-to-temporarily-show-users-a-message-when-somethin

from typing import List, Tuple
from fastapi import Request


def flash(request: Request, message: str, category: str = "message") -> None:
    request.session.setdefault("_flashes", []).append((category, message))


def get_flashed_messages(request: Request) -> List[Tuple[str, str]]:
    return request.session.pop("_flashes") if "_flashes" in request.session else []
