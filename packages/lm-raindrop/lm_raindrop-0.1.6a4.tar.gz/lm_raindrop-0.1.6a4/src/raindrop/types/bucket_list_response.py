# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["BucketListResponse", "Object"]


class Object(BaseModel):
    content_type: Optional[str] = None
    """MIME type of the object"""

    key: Optional[str] = None
    """Object key/path in the bucket"""

    last_modified: Optional[datetime] = None
    """Last modification timestamp"""

    size: Union[int, str, None] = None
    """Size of the object in bytes"""


class BucketListResponse(BaseModel):
    objects: Optional[List[Object]] = None
    """List of objects in the bucket with their metadata"""
