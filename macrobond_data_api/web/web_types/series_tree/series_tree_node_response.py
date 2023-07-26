from typing import Union, List, TypedDict


class SeriesTreeNodeResponse(TypedDict):
    nodeType: str
    """The node type. Can be one of 'leaf', 'branch', 'branchref'."""

    title: str
    """The title of the tree node"""


class SeriesTreeNodeLeaf(SeriesTreeNodeResponse):
    """Information about a node in the series database tree"""


class SeriesTreeNodeBranchRef(SeriesTreeNodeResponse):
    """Information about a node in the series database tree"""

    path: str
    """The path of the sub tree"""


class SeriesTreeNodeBranch(SeriesTreeNodeResponse):
    """Information about a node in the series database tree"""

    children: List[Union[SeriesTreeNodeLeaf, SeriesTreeNodeBranchRef]]
    """Gets the children of the tree node."""
