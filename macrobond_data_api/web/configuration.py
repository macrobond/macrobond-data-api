from typing import Type


__pdoc__ = {
    "Configuration.__init__": False,
}


class Configuration:
    """_summary_
    .. Warning:: This is only recommended for advanced users.
    """

    # WebClient
    _default_service_name = "https://apiauth.macrobondfinancial.com/mbauth/"
    _darwin_username = "Macrobond"
    _proxy_service_name = "MacrobondApiHttpProxy"
    _proxy_username = "MacrobondApiHttpProxy"

    # Session
    _default_api_url = "https://api.macrobondfinancial.com/"
    _default_authorization_url = "https://apiauth.macrobondfinancial.com/mbauth/"

    @classmethod
    def set_default_api_url(cls, val: str) -> Type["Configuration"]:
        """_summary_
        .. Warning:: This is only recommended for advanced users.
        """
        cls._default_api_url = val
        return cls

    @classmethod
    def set_default_authorization_url(cls, val: str) -> Type["Configuration"]:
        """_summary_
        .. Warning:: This is only recommended for advanced users.
        """
        cls._default_authorization_url = val
        return cls

    @classmethod
    def set_default_service_name(cls, val: str) -> Type["Configuration"]:
        """_summary_
        .. Warning:: This is only recommended for advanced users.
        """
        cls._default_service_name = val
        return cls

    @classmethod
    def set_darwin_username(cls, val: str) -> Type["Configuration"]:
        """_summary_
        .. Warning:: This is only recommended for advanced users.
        """
        cls._darwin_username = val
        return cls

    @classmethod
    def set_proxy_service_name(cls, val: str) -> Type["Configuration"]:
        """_summary_
        .. Warning:: This is only recommended for advanced users.
        """
        cls._proxy_service_name = val
        return cls

    @classmethod
    def set_proxy_username(cls, val: str) -> Type["Configuration"]:
        """_summary_
        .. Warning:: This is only recommended for advanced users.
        """
        cls._proxy_username = val
        return cls
