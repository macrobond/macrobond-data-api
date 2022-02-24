# -*- coding: utf-8 -*-

'''module doc string'''

from typing import List, TYPE_CHECKING
from abc import ABC, abstractmethod

from ._return_data_frame import _ReturnDataFrame

if TYPE_CHECKING:  # pragma: no cover

    from .metadata_attribute_information import MetadataAttributeInformation
    from .metadata_attribute_information import TypedDictMetadataAttributeInformation

    from .metadata_value_information import MetadataValueInformation
    from .metadata_value_information import TypedDictMetadataValueInformation


class ListValuesReturn(_ReturnDataFrame, ABC):

    @abstractmethod
    def list_of_objects(self) -> List['MetadataValueInformation']: ...

    @abstractmethod
    def list_of_dicts(self) -> List['TypedDictMetadataValueInformation']: ...


class GetAttributeInformationReturn(_ReturnDataFrame, ABC):

    @abstractmethod
    def object(self) -> 'MetadataAttributeInformation': ...

    @abstractmethod
    def dict(self) -> 'TypedDictMetadataAttributeInformation': ...


class MetaDirectoryMethods(ABC):
    '''
    This class fetches methods to look up metadata
    '''

    @abstractmethod
    def list_values(self, name: str) -> ListValuesReturn:
        '''
        List all metadata attribute values.

        Parameters
        ----------
        name : str
            record that failed processing

        Returns
        -------
        Converter[List[MetadataValueInformation], List[TypedDictMetadataValueInformation]]

        Examples
        -------
        ```python
        with ComClient() as api: # or WebClient
            list_of_dict = api.meta_directory.list_values('RateType').dict
            print(data_frame)
        ```
        '''

    @abstractmethod
    def get_attribute_information(self, name: str) -> GetAttributeInformationReturn:
        '''Get information about a type of metadata.'''
