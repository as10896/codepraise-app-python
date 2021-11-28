import requests
from application.views import folder_summary

from config import Settings, get_settings


class ApiGateway:
    def __init__(self, config: Settings = get_settings()):
        self._config = config

    def all_repos(self) -> str:
        return self.call_api("get", "repo")

    def repo(self, username: str, reponame: str) -> str:
        return self.call_api("get", "repo", username, reponame)

    def create_repo(self, username: str, reponame: str) -> str:
        return self.call_api("post", "repo", username, reponame)

    def delete_all_repos(self) -> str:
        return self.call_api("delete", "repo")

    def folder_summary(self, username: str, reponame: str, foldername: str) -> str:
        return self.call_api("get", "summary", username, reponame, foldername)

    def call_api(self, method: str, *resources: str) -> str:
        url_route = "/".join([self._config.API_URL, *resources])
        result: requests.models.Response = getattr(requests, method)(url_route)
        if result.status_code >= 300:
            raise Exception(result.text)
        return result.text
