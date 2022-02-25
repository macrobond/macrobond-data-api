
# CLIENT_ID = 'user name'
# CLIENT_SECRET = 'password'

from typing import List

import os
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import platform


class Credentials:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret


class CredentialsLocator:

    default_file_name = 'data-api-python_credentials.py'

    def __init__(self, paths: List[str] = None) -> None:

        if platform.system() != 'Windows':
            raise Exception('only windows is supported by CredentialsLocator')

        if not paths:
            default_file_name = self.default_file_name
            paths = [
                os.path.join(Path.home(), default_file_name),
                os.path.join('c:', default_file_name),
                os.path.join(os.getcwd(), default_file_name)
            ]
        elif len(paths) == 0:
            raise Exception('paths is an empty')

        self.__paths = paths

    def finde(self) -> Credentials:
        for path in self.__paths:
            if not os.path.isfile(path):
                continue

            spec = spec_from_file_location(
                "credentials", path
            )

            if not spec:
                continue

            module = module_from_spec(spec)

            if not spec.loader:
                continue

            spec.loader.exec_module(module)

            if not hasattr(object, 'CLIENT_ID'):
                raise Exception(f"missing 'CLIENT_ID' on file {path}")

            if not hasattr(object, 'CLIENT_SECRET'):
                raise Exception(f"missing 'CLIENT_SECRET' on file {path}")

            client_id = module.CLIENT_ID
            client_secret = module.CLIENT_SECRET

            return Credentials(client_id, client_secret)

        error = "Credentials not was not found.\npaths tried\n" + str('\n'.join(self.__paths))
        raise Exception(error)
