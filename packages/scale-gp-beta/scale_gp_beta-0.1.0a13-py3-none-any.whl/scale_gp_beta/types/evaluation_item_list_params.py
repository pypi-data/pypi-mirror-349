# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["EvaluationItemListParams"]


class EvaluationItemListParams(TypedDict, total=False):
    ending_before: str

    evaluation_id: str

    include_archived: bool

    limit: int

    starting_after: str
