# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["SpanListParams"]


class SpanListParams(TypedDict, total=False):
    ending_before: str

    from_ts: int
    """The starting (oldest) timestamp window in seconds."""

    limit: int

    parents_only: bool

    starting_after: str

    to_ts: int
    """The ending (most recent) timestamp in seconds."""

    trace_id: str
