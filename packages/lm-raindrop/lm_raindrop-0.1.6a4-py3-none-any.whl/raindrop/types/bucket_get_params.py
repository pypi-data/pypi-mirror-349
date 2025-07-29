# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["BucketGetParams"]


class BucketGetParams(TypedDict, total=False):
    key: str
    """Object key/path to download"""

    module_id: str
    """Module ID identifying the bucket"""
