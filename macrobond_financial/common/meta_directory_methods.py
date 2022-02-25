# -*- coding: utf-8 -*-

'''module doc string'''

from typing import List, Tuple, overload, Union, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

    from .metadata_attribute_information import MetadataAttributeInformation, \
        TypedDictMetadataAttributeInformation, MetadataAttributeInformationColumns

    from .metadata_value_information import MetadataValueInformation, \
        TypedDictMetadataValueInformation, MetadataValueInformationColumns


class ListValuesReturn(ABC):

    @abstractmethod
    def list_of_objects(self) -> List['MetadataValueInformation']: ...

    @abstractmethod
    def list_of_dicts(self) -> List['TypedDictMetadataValueInformation']: ...

    @overload
    def data_frame(self) -> 'DataFrame': ...

    @overload
    def data_frame(
        self,
        index: 'pandas_typing.Axes' = None,
        columns: Union[
            'MetadataValueInformationColumns', 'pandas_typing.Axes'
        ] = None,
        dtype: 'pandas_typing.Dtype' = None,
        copy: bool = False,
    ) -> 'DataFrame': ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> 'DataFrame': ...


class GetAttributeInformationReturn(ABC):

    @abstractmethod
    def object(self) -> 'MetadataAttributeInformation': ...

    @abstractmethod
    def dict(self) -> 'TypedDictMetadataAttributeInformation': ...

    @overload
    def data_frame(self) -> 'DataFrame': ...

    @overload
    def data_frame(
        self,
        index: 'pandas_typing.Axes' = None,
        columns: Union[
            'MetadataAttributeInformationColumns', 'pandas_typing.Axes'
        ] = None,
        dtype: 'pandas_typing.Dtype' = None,
        copy: bool = False,
    ) -> 'DataFrame': ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> 'DataFrame': ...


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
