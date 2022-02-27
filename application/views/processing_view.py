import re

from config import get_settings
from infrastructure import ApiResponse


# View object to capture progress bar information
class ProcessingView:
    def __init__(self, result: ApiResponse):
        self._result = result

    @property
    def ws_channel_id(self) -> str:
        return self._result.message["message"]["id"]

    @property
    def ws_host(self) -> str:
        # replace "http://" with "ws://" and "https://" with "wss://"
        return re.sub(r"^http", "ws", get_settings().API_HOST)
