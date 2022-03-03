from typing import List


class EntitieErrorInfo:
    def __init__(self, name: str, error_message: str):
        self.name = name
        self.error_message = error_message

    def __str__(self):
        return f"name: {self.name} error_message: {self.error_message}"

    def __repr__(self):
        return str(self)


class GetEntitiesError(Exception):
    def __init__(self, entities: List[EntitieErrorInfo]):
        self.entities = entities
        message = ""
        super().__init__(message)
