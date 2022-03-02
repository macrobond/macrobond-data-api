
from typing import Any, List, Union

import os
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import platform


class Credentials:

    default_file_name = 'data-api-python_credentials.py'

    def __init__(self, paths: List[str] = None) -> None:

        paths = self._get_paths(paths)

        if len(paths) == 0:
            raise Exception('paths is an empty')

        for path in paths:
            module = self._test_path(path)
            if module:
                self.client_id: str = module.CLIENT_ID
                self.client_secret: str = module.CLIENT_SECRET
                return

        error = "Credentials not was not found.\npaths tested\n" + str('\n'.join(paths))
        raise Exception(error)

    @classmethod
    def has_config(cls, paths: List[str] = None) -> bool:
        paths = cls._get_paths(paths)
        return any(cls._test_path(p) for p in paths)

    @classmethod
    def _get_paths(cls, paths: Union[List[str], None]) -> List[str]:
        if not paths:
            default_file_name = cls.default_file_name
            if cls._platform_system() == 'Windows':
                paths = [
                    cls._path_join(cls._get_home_path(), default_file_name),
                    cls._path_join('c:\\', default_file_name),
                    cls._path_join(cls._getcwd(), default_file_name)
                ]
            else:
                paths = [
                    cls._path_join(cls._get_home_path(), default_file_name),
                    cls._path_join(cls._getcwd(), default_file_name),
                ]
        return paths

    @classmethod
    def _test_path(cls, path: str) -> Any:
        if not cls._is_file(path):
            return False

        spec = spec_from_file_location(
            "credentials", path
        )

        if not spec:
            return None

        module = module_from_spec(spec)

        if not spec.loader:
            return None

        spec.loader.exec_module(module)

        if not hasattr(module, 'CLIENT_ID'):
            raise Exception(f"missing 'CLIENT_ID' in file {path}")

        if not hasattr(module, 'CLIENT_SECRET'):
            raise Exception(f"missing 'CLIENT_SECRET' in file {path}")

        return module

    @classmethod
    def _path_join(cls, *paths: str) -> str:
        return os.path.join(*paths)

    @classmethod
    def _platform_system(cls) -> str:
        return platform.system()

    @classmethod
    def _getcwd(cls) -> str:
        return os.getcwd()

    @classmethod
    def _get_home_path(cls) -> str:
        return str(Path.home())

    @classmethod
    def _is_file(cls, path: str) -> bool:
        return os.path.isfile(path)
