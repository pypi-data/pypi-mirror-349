"""Tests for the FastAPI Rate Limit package."""

import asyncio
import time
from unittest.mock import patch, AsyncMock

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from starlette.middleware import Middleware

from fastapi_rate_limit import RateLimitMiddleware, Rule, RateLimitExceeded
from fastapi_rate_limit.middleware import InMemoryStorage, PathType, RedisStorage
import redis


@pytest.fixture
def app():
    """Create a FastAPI app for testing."""
    return FastAPI()


@pytest.fixture
def memory_storage():
    """Create an in-memory storage."""
    return InMemoryStorage()


@pytest.fixture
def client(app):
    """Create a test client."""
    return TestClient(app)


def test_rule_matching():
    """Test rule path matching."""
    # Exact match
    rule = Rule(path="/test", limit=10)
    request = Request({"type": "http", "method": "GET", "path": "/test", "headers": []})
    assert rule.matches(request) is True

    request = Request(
        {"type": "http", "method": "GET", "path": "/test/123", "headers": []}
    )
    assert rule.matches(request) is False

    # Prefix match
    rule = Rule(path="/test", limit=10, path_type=PathType.PREFIX)
    request = Request({"type": "http", "method": "GET", "path": "/test", "headers": []})
    assert rule.matches(request) is True

    request = Request(
        {"type": "http", "method": "GET", "path": "/test/123", "headers": []}
    )
    assert rule.matches(request) is True

    request = Request(
        {"type": "http", "method": "GET", "path": "/other", "headers": []}
    )
    assert rule.matches(request) is False

    # Pattern match
    rule = Rule(path="/test/*", limit=10, path_type=PathType.PATTERN)
    request = Request(
        {"type": "http", "method": "GET", "path": "/test/123", "headers": []}
    )
    assert rule.matches(request) is True

    request = Request(
        {"type": "http", "method": "GET", "path": "/other/123", "headers": []}
    )
    assert rule.matches(request) is False


def test_memory_storage():
    """Test in-memory storage."""

    @pytest.mark.asyncio
    async def run_test():
        storage = InMemoryStorage()

        # Initial increment
        count = await storage.increment("test-key", 60)
        assert count == 1

        # Second increment
        count = await storage.increment("test-key", 60)
        assert count == 2

        # Check TTL
        ttl = await storage.get_ttl("test-key")
        assert 0 < ttl <= 60

        # Reset
        await storage.reset("test-key")
        count = await storage.increment("test-key", 60)
        assert count == 1

    asyncio.run(run_test())


@pytest.mark.asyncio
@patch("redis.asyncio.from_url")
async def test_redis_storage_mock(mock_redis):
    """Test Redis storage with mocks."""
    # Create mock Redis client
    mock_client = AsyncMock()
    mock_redis.return_value = mock_client

    # Create a proper async context manager for pipeline
    class MockPipeline:
        def __init__(self):
            self.incr_called = False
            self.expire_called = False

        async def incr(self, key):
            self.incr_called = True
            return self

        async def expire(self, key, period):
            self.expire_called = True
            return self

        async def execute(self):
            return [5]

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    # Setup pipeline mock
    mock_pipeline = MockPipeline()
    mock_client.pipeline.return_value = mock_pipeline

    # Mock TTL
    mock_client.ttl.return_value = 42

    # Setup delete as an awaitable
    mock_client.delete = AsyncMock()

    # Create storage
    storage = RedisStorage("redis://fakehost:6379/0")

    # Test increment
    count = await storage.increment("test-key", 60)
    assert count == 5
    assert mock_pipeline.incr_called
    assert mock_pipeline.expire_called

    # Test TTL
    ttl = await storage.get_ttl("test-key")
    assert ttl == 42
    mock_client.ttl.assert_called_once()

    # Test reset
    await storage.reset("test-key")
    mock_client.delete.assert_called_once_with("test-key")


@pytest.mark.asyncio
async def test_redis_storage_error_handling():
    """Test Redis storage error handling."""
    # Create a mock Redis client that raises errors
    mock_client = AsyncMock()

    # Create a pipeline that raises errors
    class ErrorPipeline:
        async def incr(self, key):
            raise redis.RedisError("Connection error")

        async def expire(self, key, period):
            raise redis.RedisError("Connection error")

        async def execute(self):
            raise redis.RedisError("Connection error")

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    mock_client.pipeline.return_value = ErrorPipeline()
    mock_client.ttl.side_effect = redis.RedisError("Connection error")
    mock_client.delete.side_effect = redis.RedisError("Connection error")

    # Create storage with mock client
    storage = RedisStorage("redis://fakehost:6379/0")
    storage.redis = mock_client

    # Test increment with error
    count = await storage.increment("test-key", 60)
    assert count == 0

    # Test TTL with error
    ttl = await storage.get_ttl("test-key")
    assert ttl == 0

    # Test reset with error
    await storage.reset("test-key")  # Should not raise


def test_middleware_basic(app, client):
    """Test basic middleware functionality."""

    # Add test route
    @app.get("/test")
    async def test_route():
        return {"message": "success"}

    # Add middleware with a simple rule
    app.add_middleware(
        RateLimitMiddleware, rules=[Rule(path="/test", limit=2, period=5)]
    )

    # First request should pass
    response = client.get("/test")
    assert response.status_code == 200
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert int(response.headers["X-RateLimit-Remaining"]) == 1

    # Second request should pass
    response = client.get("/test")
    assert response.status_code == 200
    assert int(response.headers["X-RateLimit-Remaining"]) == 0

    # Third request should be rate limited
    response = client.get("/test")
    assert response.status_code == 429
    assert "detail" in response.json()
    assert "retry_after" in response.json()
    assert "Retry-After" in response.headers


def test_middleware_path_types(app, client):
    """Test middleware with different path types."""

    # Add test routes
    @app.get("/api/v1/items")
    async def get_items():
        return {"items": ["item1", "item2"]}

    @app.get("/api/v1/users")
    async def get_users():
        return {"users": ["user1", "user2"]}

    # Add middleware with a prefix rule
    app.add_middleware(
        RateLimitMiddleware,
        rules=[Rule(path="/api/v1", limit=2, period=5, path_type=PathType.PREFIX)],
    )

    # First request to items should pass
    response = client.get("/api/v1/items")
    assert response.status_code == 200

    # First request to users should pass (but counts toward the same limit)
    response = client.get("/api/v1/users")
    assert response.status_code == 200

    # Third request to any API endpoint should be rate limited
    response = client.get("/api/v1/items")
    assert response.status_code == 429


def test_custom_exception_handler(app, client):
    """Test middleware with custom exception handler."""

    # Add test route
    @app.get("/test")
    async def test_route():
        return {"message": "success"}

    # Custom exception handler
    async def custom_handler(request, exc):
        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=429,
            content={"custom_error": "Too many requests", "wait_for": exc.retry_after},
            headers={"X-Custom-Header": "rate-limited"},
        )

    # Add middleware with custom handler
    app.add_middleware(
        RateLimitMiddleware,
        rules=[Rule(path="/test", limit=1, period=5)],
        exception_handler=custom_handler,
    )

    # First request should pass
    response = client.get("/test")
    assert response.status_code == 200

    # Second request should use custom handler
    response = client.get("/test")
    assert response.status_code == 429
    assert "custom_error" in response.json()
    assert response.headers["X-Custom-Header"] == "rate-limited"


def test_middleware_headers(app, client):
    """Test middleware response headers."""

    @app.get("/test")
    async def test_route():
        return {"message": "success"}

    app.add_middleware(
        RateLimitMiddleware, rules=[Rule(path="/test", limit=2, period=5)]
    )

    # First request
    response = client.get("/test")
    assert response.status_code == 200
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert "X-RateLimit-Reset" in response.headers
    assert int(response.headers["X-RateLimit-Limit"]) == 2
    assert int(response.headers["X-RateLimit-Remaining"]) == 1

    # Second request
    response = client.get("/test")
    assert response.status_code == 200
    assert int(response.headers["X-RateLimit-Remaining"]) == 0

    # Third request (rate limited)
    response = client.get("/test")
    assert response.status_code == 429
    assert "Retry-After" in response.headers
    assert "X-RateLimit-Limit" in response.headers
    assert "X-RateLimit-Remaining" in response.headers
    assert "X-RateLimit-Reset" in response.headers
