class AuthBaseException(Exception):
    pass


class AuthDiscoveryException(AuthBaseException):
    pass


class AuthFetchTokenException(AuthBaseException):
    pass


class AuthInvalidCredentialsException(AuthFetchTokenException):
    pass


class AuthTooManyRequestsException(AuthBaseException):

    @property
    def retry_after(self) -> int:
        """
        retry-after indicate how long a client should wait before making the request again.
        this is in seconds.
        """
        return self._retry_after

    def __init__(self, message: str, retry_after: int) -> None:
        super().__init__(message)
        self._retry_after = retry_after
