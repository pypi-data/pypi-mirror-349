# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["BucketDeleteParams"]


class BucketDeleteParams(TypedDict, total=False):
    key: Required[str]
    """Object key/path to delete"""

    module_id: Required[Annotated[str, PropertyInfo(alias="moduleId")]]
    """Module ID identifying the bucket"""
