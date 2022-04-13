from typing import cast, List, Union, Optional, TYPE_CHECKING
import os
import json
from pathlib import Path
import platform
from typing_extensions import Literal, TypedDict

if TYPE_CHECKING:

    class CredentialsJsonObj(TypedDict):
        clientId: str
        clientSecret: str
        apiUrl: Optional[str]
        authorizationUrl: Optional[str]


class Credentials:

    default_file_name = "mb_data_api_credentials.json"

    def __init__(self, paths: List[str] = None) -> None:

        paths = self._get_paths(paths)

        if len(paths) == 0:
            raise Exception("paths is an empty")

        for path in paths:
            json_obj = self._test_path(path)
            if json_obj:
                self.client_id = json_obj["clientId"]
                self.client_secret = json_obj["clientSecret"]
                self.api_url = json_obj.get("apiUrl")
                self.authorization_url = json_obj.get("authorizationUrl")
                return

        error = "Credentials not was not found.\npaths tested\n" + str("\n".join(paths))
        raise Exception(error)

    @classmethod
    def has_config(cls, paths: List[str] = None) -> bool:
        paths = cls._get_paths(paths)
        return any(cls._test_path(p) for p in paths)

    @classmethod
    def _get_paths(cls, paths: Union[List[str], None]) -> List[str]:
        if not paths:
            default_file_name = cls.default_file_name
            paths = [
                cls._path_join(cls._get_home_path(), default_file_name),
                cls._path_join(cls._getcwd(), default_file_name),
                cls._path_join(cls._get_root_path(), default_file_name),
            ]
        return paths

    @classmethod
    def _test_path(cls, path: str) -> Union[Literal[False], "CredentialsJsonObj"]:
        if not cls._is_file(path):
            return False

        json_obj: CredentialsJsonObj
        with open(path, "r", encoding="utf-8") as file:
            json_obj = cast("CredentialsJsonObj", json.loads(file.read()))

        if not isinstance(json_obj, dict):
            raise Exception(f"no json obj in file {path}")

        if "clientId" not in json_obj:
            raise Exception(f"missing 'clientId' in file {path}")

        if not isinstance(json_obj["clientId"], str):
            raise Exception(f"clientId is not a string in file {path}")

        if "clientSecret" not in json_obj:
            raise Exception(f"missing 'clientSecret' in file {path}")

        if not isinstance(json_obj["clientSecret"], str):
            raise Exception(f"clientSecret is not a string in file {path}")

        return json_obj

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

    @classmethod
    def _get_root_path(cls) -> str:
        return os.path.abspath(os.sep)
