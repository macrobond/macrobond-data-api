# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from requests import Response  # type: ignore


class HttpException(Exception):

    response: "Response"

    def __init__(self, response: "Response") -> None:
        request = response.request
        super().__init__(
            (
                f"http {request.method} request to {request.path_url} "
                f"returnd status_code: {str(response.status_code)} "
                f'text: "{response.text}"'
            )
        )
        self.response = response
