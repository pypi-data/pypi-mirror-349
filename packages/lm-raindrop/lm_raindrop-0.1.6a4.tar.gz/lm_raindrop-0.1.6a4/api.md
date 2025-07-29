# Query

Types:

```python
from raindrop.types import (
    BucketLocator,
    QueryChunkSearchResponse,
    QueryDocumentQueryResponse,
    QueryGetPaginatedSearchResponse,
    QuerySearchResponse,
    QuerySumarizePageResponse,
)
```

Methods:

- <code title="post /v1/chunk_search">client.query.<a href="./src/raindrop/resources/query.py">chunk_search</a>(\*\*<a href="src/raindrop/types/query_chunk_search_params.py">params</a>) -> <a href="./src/raindrop/types/query_chunk_search_response.py">QueryChunkSearchResponse</a></code>
- <code title="post /v1/document_query">client.query.<a href="./src/raindrop/resources/query.py">document_query</a>(\*\*<a href="src/raindrop/types/query_document_query_params.py">params</a>) -> <a href="./src/raindrop/types/query_document_query_response.py">QueryDocumentQueryResponse</a></code>
- <code title="post /v1/get_paginated_results">client.query.<a href="./src/raindrop/resources/query.py">get_paginated_search</a>(\*\*<a href="src/raindrop/types/query_get_paginated_search_params.py">params</a>) -> <a href="./src/raindrop/types/query_get_paginated_search_response.py">QueryGetPaginatedSearchResponse</a></code>
- <code title="post /v1/search">client.query.<a href="./src/raindrop/resources/query.py">search</a>(\*\*<a href="src/raindrop/types/query_search_params.py">params</a>) -> <a href="./src/raindrop/types/query_search_response.py">QuerySearchResponse</a></code>
- <code title="post /v1/summarize_page">client.query.<a href="./src/raindrop/resources/query.py">sumarize_page</a>(\*\*<a href="src/raindrop/types/query_sumarize_page_params.py">params</a>) -> <a href="./src/raindrop/types/query_sumarize_page_response.py">QuerySumarizePageResponse</a></code>

# Bucket

Types:

```python
from raindrop.types import (
    BucketListResponse,
    BucketDeleteResponse,
    BucketGetResponse,
    BucketPutResponse,
)
```

Methods:

- <code title="post /v1/list_objects">client.bucket.<a href="./src/raindrop/resources/bucket.py">list</a>(\*\*<a href="src/raindrop/types/bucket_list_params.py">params</a>) -> <a href="./src/raindrop/types/bucket_list_response.py">BucketListResponse</a></code>
- <code title="post /v1/delete_object">client.bucket.<a href="./src/raindrop/resources/bucket.py">delete</a>(\*\*<a href="src/raindrop/types/bucket_delete_params.py">params</a>) -> <a href="./src/raindrop/types/bucket_delete_response.py">object</a></code>
- <code title="post /v1/get_object">client.bucket.<a href="./src/raindrop/resources/bucket.py">get</a>(\*\*<a href="src/raindrop/types/bucket_get_params.py">params</a>) -> <a href="./src/raindrop/types/bucket_get_response.py">BucketGetResponse</a></code>
- <code title="post /v1/put_object">client.bucket.<a href="./src/raindrop/resources/bucket.py">put</a>(\*\*<a href="src/raindrop/types/bucket_put_params.py">params</a>) -> <a href="./src/raindrop/types/bucket_put_response.py">BucketPutResponse</a></code>
