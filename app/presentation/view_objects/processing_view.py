import re

from config import get_settings

from ...infrastructure import ApiResponse


# View object to capture progress bar information
class ProcessingView:
    def __init__(self, result: ApiResponse):
        self._result = result

    @property
    def ws_channel_id(self) -> str:
        return self._result.message["message"]["id"]

    @property
    def ws_host(self) -> str:
        # If API is hosted locally with Docker, replace "host.docker.internal" with "localhost"
        # since JavaScript running in the browser can't resolve "host.docker.internal"
        _ws_host = re.sub("host.docker.internal", "localhost", get_settings().API_HOST)

        # replace "http://" with "ws://" and "https://" with "wss://"
        _ws_host = re.sub(r"^http", "ws", _ws_host)

        return _ws_host
