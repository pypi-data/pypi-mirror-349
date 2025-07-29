# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["QueryGetPaginatedSearchParams"]


class QueryGetPaginatedSearchParams(TypedDict, total=False):
    page: Required[Optional[int]]
    """Requested page number"""

    page_size: Required[Optional[int]]
    """Results per page"""

    request_id: Required[str]
    """Original search session identifier from the initial search"""
