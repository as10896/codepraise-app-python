from typing import Any, Dict

from returns.pipeline import flow
from returns.pointfree import bind
from returns.result import Failure, Result, Success

from ...infrastructure import ApiGateway, ApiResponse
from ..forms import URLRequest


class AddProject:
    def __call__(self, input: URLRequest) -> Result[Dict[str, Any], str]:
        return flow(
            input,
            self.validate_input,
            bind(self.add_project),
        )

    def validate_input(self, input: URLRequest) -> Result[Dict[str, Any], str]:
        if input.success:
            ownername, reponame = input.url.split("/")[-2:]
            return Success({"ownername": ownername, "reponame": reponame})
        else:
            return Failure("; ".join(input.errors.values()))

    def add_project(self, input: Dict[str, Any]) -> Result[Dict[str, Any], str]:
        result: ApiResponse = ApiGateway().create_repo(
            input["ownername"], input["reponame"]
        )
        if result.failure:
            return Failure(result.message["error"])
        return Success(input)
