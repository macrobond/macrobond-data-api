class AuthBaseException(Exception):
    pass


class AuthDiscoveryException(AuthBaseException):
    pass


class AuthFetchTokenException(AuthBaseException):
    pass


class AuthInvalidCredentialsException(AuthFetchTokenException):
    pass
