from typing import Dict, List, Optional, Tuple, Iterable, cast, Union

__pdoc__ = {
    "EntitieErrorInfo.__init__": False,
    "GetEntitiesError.__init__": False,
}


class EntitieErrorInfo:
    def __init__(self, name: str, error_message: str):
        self.name = name
        self.error_message = error_message

    def __str__(self):
        return f"name: {self.name} error_message: {self.error_message}"

    def __repr__(self):
        return str(self)


class GetEntitiesError(Exception):
    def __init__(
        self,
        entities: Union[List[EntitieErrorInfo], str, Dict[str, str]],
        error_message: str = None,
    ):
        if isinstance(entities, list):
            self.entities = entities
        elif isinstance(entities, dict):
            self.entities = list(map(EntitieErrorInfo, entities.keys(), entities.values()))
        else:
            self.entities = [EntitieErrorInfo(entities, cast(str, error_message))]

        self.message = "failed to retrieve:\n" + (
            "\n".join(
                map(
                    lambda x: "\t" + x.name + " error_message: " + x.error_message,
                    self.entities,
                )
            )
        )
        super().__init__(self.message)

    @classmethod
    def raise_if(
        cls,
        raise_error: bool,
        entities_or_name: Union[Iterable[Tuple[str, Optional[str]]], str],
        error_message: str = None,
    ) -> None:
        if not raise_error:
            return

        if isinstance(entities_or_name, str):
            if error_message:
                name = entities_or_name
                raise GetEntitiesError(name, error_message)
        else:
            entities = entities_or_name
            entities_list = cast(
                List[Tuple[str, str]],
                list(filter(lambda x: x[1] is not None, entities)),
            )
            if entities_list:
                raise GetEntitiesError(
                    list(map(lambda x: EntitieErrorInfo(x[0], x[1]), entities_list))
                )
