class AuthBaseError(Exception):
    pass


class AuthDiscoveryError(AuthBaseError):
    pass


class AuthFetchTokenError(AuthBaseError):
    pass


class AuthInvalidCredentialsError(AuthFetchTokenError):
    pass
