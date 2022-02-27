import json
from typing import Any, Dict

import requests

from config import Settings, get_settings


class ApiResponse:
    HTTP_STATUS = {
        200: "ok",
        201: "created",
        202: "processing",
        204: "no_content",
        403: "forbidden",
        404: "not_found",
        400: "bad_request",
        409: "conflict",
        422: "cannot_process",
        500: "internal_error",
    }

    def __init__(self, code: int, message: str):
        self._code = code
        self._message = message
        self._status = self.HTTP_STATUS[code]

    @property
    def success(self) -> True:
        return 200 <= self._code <= 299

    @property
    def failure(self) -> True:
        return not self.success

    @property
    def code(self) -> int:
        return self._code

    @property
    def message(self) -> Dict[str, Any]:
        return json.loads(self._message)

    @property
    def ok(self) -> bool:
        return self._status == "ok"

    @property
    def processing(self) -> bool:
        return self._status == "processing"


class ApiGateway:
    def __init__(self, config: Settings = get_settings()):
        self._config = config

    def all_repos(self) -> ApiResponse:
        return self.call_api("get", "repo")

    def repo(self, username: str, reponame: str) -> ApiResponse:
        return self.call_api("get", "repo", username, reponame)

    def create_repo(self, username: str, reponame: str) -> ApiResponse:
        return self.call_api("post", "repo", username, reponame)

    def delete_all_repos(self) -> ApiResponse:
        return self.call_api("delete", "repo")

    def folder_summary(
        self, username: str, reponame: str, foldername: str
    ) -> ApiResponse:
        return self.call_api("get", "summary", username, reponame, foldername)

    def call_api(self, method: str, *resources: str) -> ApiResponse:
        url_route = "/".join([self._config.API_HOST, self._config.API_VER, *resources])
        result: requests.models.Response = getattr(requests, method)(url_route)
        return ApiResponse(result.status_code, result.text)
