from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from requests import Response


class _ResponseAsFileObject:
    def __init__(self, response: "Response", chunk_size: int = 65536) -> None:
        self.data = response.iter_content(chunk_size=chunk_size)

    def read(self, n: int) -> bytes:
        if n == 0:
            return b""
        return next(self.data, b"")
