# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from raindrop import Raindrop, AsyncRaindrop
from tests.utils import assert_matches_type
from raindrop.types import (
    BucketGetResponse,
    BucketPutResponse,
    BucketListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBucket:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Raindrop) -> None:
        bucket = client.bucket.list()
        assert_matches_type(BucketListResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Raindrop) -> None:
        bucket = client.bucket.list(
            module_id="01jtgtrd37acrqf7k24dggg31s",
        )
        assert_matches_type(BucketListResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Raindrop) -> None:
        response = client.bucket.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bucket = response.parse()
        assert_matches_type(BucketListResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Raindrop) -> None:
        with client.bucket.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bucket = response.parse()
            assert_matches_type(BucketListResponse, bucket, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Raindrop) -> None:
        bucket = client.bucket.delete()
        assert_matches_type(object, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_delete_with_all_params(self, client: Raindrop) -> None:
        bucket = client.bucket.delete(
            key="my-key",
            module_id="01jtgtrd37acrqf7k24dggg31s",
        )
        assert_matches_type(object, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Raindrop) -> None:
        response = client.bucket.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bucket = response.parse()
        assert_matches_type(object, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Raindrop) -> None:
        with client.bucket.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bucket = response.parse()
            assert_matches_type(object, bucket, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get(self, client: Raindrop) -> None:
        bucket = client.bucket.get()
        assert_matches_type(BucketGetResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_with_all_params(self, client: Raindrop) -> None:
        bucket = client.bucket.get(
            key="my-key",
            module_id="01jtgtrd37acrqf7k24dggg31s",
        )
        assert_matches_type(BucketGetResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get(self, client: Raindrop) -> None:
        response = client.bucket.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bucket = response.parse()
        assert_matches_type(BucketGetResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get(self, client: Raindrop) -> None:
        with client.bucket.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bucket = response.parse()
            assert_matches_type(BucketGetResponse, bucket, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_put(self, client: Raindrop) -> None:
        bucket = client.bucket.put(
            content="U3RhaW5sZXNzIHJvY2tz",
        )
        assert_matches_type(BucketPutResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_put_with_all_params(self, client: Raindrop) -> None:
        bucket = client.bucket.put(
            content="U3RhaW5sZXNzIHJvY2tz",
            content_type="application/pdf",
            key="my-key",
            module_id="01jtgtrd37acrqf7k24dggg31s",
        )
        assert_matches_type(BucketPutResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_put(self, client: Raindrop) -> None:
        response = client.bucket.with_raw_response.put(
            content="U3RhaW5sZXNzIHJvY2tz",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bucket = response.parse()
        assert_matches_type(BucketPutResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_put(self, client: Raindrop) -> None:
        with client.bucket.with_streaming_response.put(
            content="U3RhaW5sZXNzIHJvY2tz",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bucket = response.parse()
            assert_matches_type(BucketPutResponse, bucket, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBucket:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncRaindrop) -> None:
        bucket = await async_client.bucket.list()
        assert_matches_type(BucketListResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRaindrop) -> None:
        bucket = await async_client.bucket.list(
            module_id="01jtgtrd37acrqf7k24dggg31s",
        )
        assert_matches_type(BucketListResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.bucket.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bucket = await response.parse()
        assert_matches_type(BucketListResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRaindrop) -> None:
        async with async_client.bucket.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bucket = await response.parse()
            assert_matches_type(BucketListResponse, bucket, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncRaindrop) -> None:
        bucket = await async_client.bucket.delete()
        assert_matches_type(object, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncRaindrop) -> None:
        bucket = await async_client.bucket.delete(
            key="my-key",
            module_id="01jtgtrd37acrqf7k24dggg31s",
        )
        assert_matches_type(object, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.bucket.with_raw_response.delete()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bucket = await response.parse()
        assert_matches_type(object, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncRaindrop) -> None:
        async with async_client.bucket.with_streaming_response.delete() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bucket = await response.parse()
            assert_matches_type(object, bucket, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get(self, async_client: AsyncRaindrop) -> None:
        bucket = await async_client.bucket.get()
        assert_matches_type(BucketGetResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_with_all_params(self, async_client: AsyncRaindrop) -> None:
        bucket = await async_client.bucket.get(
            key="my-key",
            module_id="01jtgtrd37acrqf7k24dggg31s",
        )
        assert_matches_type(BucketGetResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.bucket.with_raw_response.get()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bucket = await response.parse()
        assert_matches_type(BucketGetResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncRaindrop) -> None:
        async with async_client.bucket.with_streaming_response.get() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bucket = await response.parse()
            assert_matches_type(BucketGetResponse, bucket, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_put(self, async_client: AsyncRaindrop) -> None:
        bucket = await async_client.bucket.put(
            content="U3RhaW5sZXNzIHJvY2tz",
        )
        assert_matches_type(BucketPutResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_put_with_all_params(self, async_client: AsyncRaindrop) -> None:
        bucket = await async_client.bucket.put(
            content="U3RhaW5sZXNzIHJvY2tz",
            content_type="application/pdf",
            key="my-key",
            module_id="01jtgtrd37acrqf7k24dggg31s",
        )
        assert_matches_type(BucketPutResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_put(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.bucket.with_raw_response.put(
            content="U3RhaW5sZXNzIHJvY2tz",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        bucket = await response.parse()
        assert_matches_type(BucketPutResponse, bucket, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_put(self, async_client: AsyncRaindrop) -> None:
        async with async_client.bucket.with_streaming_response.put(
            content="U3RhaW5sZXNzIHJvY2tz",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            bucket = await response.parse()
            assert_matches_type(BucketPutResponse, bucket, path=["response"])

        assert cast(Any, response.is_closed) is True
