# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from datetime import datetime
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._utils import PropertyInfo

__all__ = ["SpanCreateParams", "BaseSpanCreateRequest", "LegacyApplicationSpanCreateRequest"]


class BaseSpanCreateRequest(TypedDict, total=False):
    name: Required[str]

    start_timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    trace_id: Required[str]
    """id for grouping traces together, uuid is recommended"""

    end_timestamp: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    input: Dict[str, object]

    metadata: Dict[str, object]

    output: Dict[str, object]

    parent_id: str
    """Reference to a parent span_id"""

    status: Literal["SUCCESS", "ERROR"]

    type: str


class LegacyApplicationSpanCreateRequest(TypedDict, total=False):
    application_interaction_id: Required[str]

    application_variant_id: Required[str]

    name: Required[str]

    start_timestamp: Required[Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]]

    trace_id: Required[str]
    """id for grouping traces together, uuid is recommended"""

    end_timestamp: Annotated[Union[str, datetime], PropertyInfo(format="iso8601")]

    input: Dict[str, object]

    metadata: Dict[str, object]

    output: Dict[str, object]

    parent_id: str
    """Reference to a parent span_id"""

    status: Literal["SUCCESS", "ERROR"]

    type: str


SpanCreateParams: TypeAlias = Union[BaseSpanCreateRequest, LegacyApplicationSpanCreateRequest]
