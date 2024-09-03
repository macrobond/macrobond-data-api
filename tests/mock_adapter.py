from unittest.mock import Mock
from typing import Any, List

from requests import Response
from requests.adapters import BaseAdapter


class MockAdapter(BaseAdapter):

    def __init__(self, responses: List[Response], urls: List[str]) -> None:
        self.mock = Mock()
        self.mock.send.side_effect = responses
        self.index = 0
        self.urls_expected = urls
        self.ulrs_actual: List[str] = []

        assert len(responses) == len(urls)

        super().__init__()

    def send(
        self,
        request: Any,
        stream: Any = False,
        timeout: Any = None,
        verify: Any = True,
        cert: Any = None,
        proxies: Any = None,
    ) -> Response:

        if self.index >= len(self.urls_expected):
            raise ValueError("Too many requests urls:", request.url)

        assert self.urls_expected[self.index] == request.url, (
            "\n" + "\n".join(self.urls_expected) + f"\n index: {str(self.index)}"
        )

        self.index += 1

        response = self.mock.send()
        assert response is not None
        return response

    def close(self) -> None:
        pass

    def assert_this(self) -> None:
        assert len(self.urls_expected) != 0
        assert len(self.urls_expected) == self.index
