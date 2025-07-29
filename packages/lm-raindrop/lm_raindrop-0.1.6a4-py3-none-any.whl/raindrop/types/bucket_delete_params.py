# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["BucketDeleteParams"]


class BucketDeleteParams(TypedDict, total=False):
    key: str
    """Object key/path to delete"""

    module_id: str
    """Module ID identifying the bucket"""
