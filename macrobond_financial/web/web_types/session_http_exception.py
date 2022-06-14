# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from requests import Response  # type: ignore


class SessionHttpException(Exception):
    @property
    def status_code(self) -> int:
        return self.__response.status_code

    @property
    def response(self) -> "Response":
        return self.__response

    def __init__(self, response: "Response") -> None:
        request = response.request
        super().__init__(
            (
                f"http {request.method} request to {request.path_url} "
                f"returnd status_code: {str(response.status_code)} "
                f'text: "{response.text}"'
            )
        )
        self.__response = response
