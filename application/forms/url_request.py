import re
from typing import Dict
from fastapi import Form


class URLRequest:
    URL_REGEX = r"^http[s]?://github\.com/.*/.*(?<!git)$"

    def __init__(self, url: str = Form(...)):
        self._errors = {}
        if re.match(self.URL_REGEX, url):
            self.url = url
        else:
            self._errors["url"] = "Invalid address for a Github project"

    @property
    def success(self) -> bool:
        return len(self._errors) == 0

    @property
    def errors(self) -> Dict[str, str]:
        return self._errors
