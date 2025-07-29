# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union

import httpx

from ..types import bucket_get_params, bucket_put_params, bucket_list_params, bucket_delete_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven, Base64FileInput
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.bucket_get_response import BucketGetResponse
from ..types.bucket_put_response import BucketPutResponse
from ..types.bucket_list_response import BucketListResponse

__all__ = ["BucketResource", "AsyncBucketResource"]


class BucketResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BucketResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return BucketResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BucketResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#with_streaming_response
        """
        return BucketResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        module_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BucketListResponse:
        """List all objects in a SmartBucket or regular bucket.

        The bucket parameter (ID)
        is used to identify the bucket to list objects from.

        Args:
          module_id: Module ID identifying the bucket

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/list_objects",
            body=maybe_transform({"module_id": module_id}, bucket_list_params.BucketListParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BucketListResponse,
        )

    def delete(
        self,
        *,
        key: str | NotGiven = NOT_GIVEN,
        module_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Delete a file from a SmartBucket or regular bucket.

        The bucket parameter (ID) is
        used to identify the bucket to delete from. The key is the path to the object in
        the bucket.

        Args:
          key: Object key/path to delete

          module_id: Module ID identifying the bucket

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/delete_object",
            body=maybe_transform(
                {
                    "key": key,
                    "module_id": module_id,
                },
                bucket_delete_params.BucketDeleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def get(
        self,
        *,
        key: str | NotGiven = NOT_GIVEN,
        module_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BucketGetResponse:
        """Download a file from a SmartBucket or regular bucket.

        The bucket parameter (ID)
        is used to identify the bucket to download from. The key is the path to the
        object in the bucket.

        Args:
          key: Object key/path to download

          module_id: Module ID identifying the bucket

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/get_object",
            body=maybe_transform(
                {
                    "key": key,
                    "module_id": module_id,
                },
                bucket_get_params.BucketGetParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BucketGetResponse,
        )

    def put(
        self,
        *,
        content: Union[str, Base64FileInput],
        content_type: str | NotGiven = NOT_GIVEN,
        key: str | NotGiven = NOT_GIVEN,
        module_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BucketPutResponse:
        """Upload a file to a SmartBucket or regular bucket.

        The bucket parameter (ID) is
        used to identify the bucket to upload to. The key is the path to the object in
        the bucket.

        Args:
          content: Binary content of the object

          content_type: MIME type of the object

          key: Object key/path in the bucket

          module_id: Module ID identifying the bucket

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/put_object",
            body=maybe_transform(
                {
                    "content": content,
                    "content_type": content_type,
                    "key": key,
                    "module_id": module_id,
                },
                bucket_put_params.BucketPutParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BucketPutResponse,
        )


class AsyncBucketResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBucketResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncBucketResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBucketResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/lm-raindrop-python-sdk#with_streaming_response
        """
        return AsyncBucketResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        module_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BucketListResponse:
        """List all objects in a SmartBucket or regular bucket.

        The bucket parameter (ID)
        is used to identify the bucket to list objects from.

        Args:
          module_id: Module ID identifying the bucket

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/list_objects",
            body=await async_maybe_transform({"module_id": module_id}, bucket_list_params.BucketListParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BucketListResponse,
        )

    async def delete(
        self,
        *,
        key: str | NotGiven = NOT_GIVEN,
        module_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Delete a file from a SmartBucket or regular bucket.

        The bucket parameter (ID) is
        used to identify the bucket to delete from. The key is the path to the object in
        the bucket.

        Args:
          key: Object key/path to delete

          module_id: Module ID identifying the bucket

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/delete_object",
            body=await async_maybe_transform(
                {
                    "key": key,
                    "module_id": module_id,
                },
                bucket_delete_params.BucketDeleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def get(
        self,
        *,
        key: str | NotGiven = NOT_GIVEN,
        module_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BucketGetResponse:
        """Download a file from a SmartBucket or regular bucket.

        The bucket parameter (ID)
        is used to identify the bucket to download from. The key is the path to the
        object in the bucket.

        Args:
          key: Object key/path to download

          module_id: Module ID identifying the bucket

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/get_object",
            body=await async_maybe_transform(
                {
                    "key": key,
                    "module_id": module_id,
                },
                bucket_get_params.BucketGetParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BucketGetResponse,
        )

    async def put(
        self,
        *,
        content: Union[str, Base64FileInput],
        content_type: str | NotGiven = NOT_GIVEN,
        key: str | NotGiven = NOT_GIVEN,
        module_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BucketPutResponse:
        """Upload a file to a SmartBucket or regular bucket.

        The bucket parameter (ID) is
        used to identify the bucket to upload to. The key is the path to the object in
        the bucket.

        Args:
          content: Binary content of the object

          content_type: MIME type of the object

          key: Object key/path in the bucket

          module_id: Module ID identifying the bucket

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/put_object",
            body=await async_maybe_transform(
                {
                    "content": content,
                    "content_type": content_type,
                    "key": key,
                    "module_id": module_id,
                },
                bucket_put_params.BucketPutParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BucketPutResponse,
        )


class BucketResourceWithRawResponse:
    def __init__(self, bucket: BucketResource) -> None:
        self._bucket = bucket

        self.list = to_raw_response_wrapper(
            bucket.list,
        )
        self.delete = to_raw_response_wrapper(
            bucket.delete,
        )
        self.get = to_raw_response_wrapper(
            bucket.get,
        )
        self.put = to_raw_response_wrapper(
            bucket.put,
        )


class AsyncBucketResourceWithRawResponse:
    def __init__(self, bucket: AsyncBucketResource) -> None:
        self._bucket = bucket

        self.list = async_to_raw_response_wrapper(
            bucket.list,
        )
        self.delete = async_to_raw_response_wrapper(
            bucket.delete,
        )
        self.get = async_to_raw_response_wrapper(
            bucket.get,
        )
        self.put = async_to_raw_response_wrapper(
            bucket.put,
        )


class BucketResourceWithStreamingResponse:
    def __init__(self, bucket: BucketResource) -> None:
        self._bucket = bucket

        self.list = to_streamed_response_wrapper(
            bucket.list,
        )
        self.delete = to_streamed_response_wrapper(
            bucket.delete,
        )
        self.get = to_streamed_response_wrapper(
            bucket.get,
        )
        self.put = to_streamed_response_wrapper(
            bucket.put,
        )


class AsyncBucketResourceWithStreamingResponse:
    def __init__(self, bucket: AsyncBucketResource) -> None:
        self._bucket = bucket

        self.list = async_to_streamed_response_wrapper(
            bucket.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            bucket.delete,
        )
        self.get = async_to_streamed_response_wrapper(
            bucket.get,
        )
        self.put = async_to_streamed_response_wrapper(
            bucket.put,
        )
