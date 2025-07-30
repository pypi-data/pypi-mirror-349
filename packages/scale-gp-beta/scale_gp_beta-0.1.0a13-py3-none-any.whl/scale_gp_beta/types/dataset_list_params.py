# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["DatasetListParams"]


class DatasetListParams(TypedDict, total=False):
    ending_before: str

    include_archived: bool

    limit: int

    name: str

    starting_after: str

    tags: List[str]
