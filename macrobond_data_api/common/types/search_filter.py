from dataclasses import dataclass
from typing import Dict, Sequence, Union


@dataclass(init=False)
class SearchFilter:
    __slots__ = (
        "text",
        "entity_types",
        "must_have_values",
        "must_not_have_values",
        "must_have_attributes",
        "must_not_have_attributes",
    )

    def __init__(
        self,
        text: str = None,
        entity_types: Union[Sequence[str], str] = None,
        must_have_values: Dict[str, object] = None,
        must_not_have_values: Dict[str, object] = None,
        must_have_attributes: Union[Sequence[str], str] = None,
        must_not_have_attributes: Union[Sequence[str], str] = None,
    ) -> None:
        """
        Specification of a search filter.

        Parameters
        ----------
        text: str
            Optional set of keywords separated by space.
        must_have_values: Dict[str, object]
            Optional dictionary of values that must be present in the entity metadata.
            The value can be a single value or an array of values. If there are several values
            for an attribute, it means that either of them must be present.
        must_not_have_values: Dict[str, object]
            Optional dictionary of values that must not be present in the entity metadata.
            The value can be a single value or an array of values.
        must_have_attributes: Union[Sequence[str], str]
            Optional set of attributes that must be present in the entity metadata.
            The value can be a single value or a sequence of values.
        must_not_have_attributes: Union[Sequence[str], str]
            Optional set of attributes that must no be present in the entity metadata.
            The value can be a single value or a sequence of values.
        """
        self.text = text

        if isinstance(entity_types, str):
            self.entity_types: Sequence[str] = [entity_types]
        else:
            self.entity_types = entity_types if entity_types else []

        self.must_have_values: Dict[str, object] = must_have_values if must_have_values else {}

        self.must_not_have_values: Dict[str, object] = must_not_have_values if must_not_have_values else {}

        if isinstance(must_have_attributes, str):
            self.must_have_attributes: Sequence[str] = [must_have_attributes]
        else:
            self.must_have_attributes = must_have_attributes if must_have_attributes else []

        if isinstance(must_not_have_attributes, str):
            self.must_not_have_attributes: Sequence[str] = [must_not_have_attributes]
        else:
            self.must_not_have_attributes = must_not_have_attributes if must_not_have_attributes else []
