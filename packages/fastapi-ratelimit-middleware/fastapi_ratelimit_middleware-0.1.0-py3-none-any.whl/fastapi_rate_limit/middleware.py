"""Rate limiting middleware for FastAPI applications."""

import asyncio
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, Dict, List, Optional, Pattern, Set, Union
import re

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp
import redis.asyncio as redis
from pydantic import BaseModel, Field


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, limit: int, period: int, retry_after: int):
        self.limit = limit
        self.period = period
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded: {limit} requests per {period} seconds")


class PathType(str, Enum):
    """Type of path matching."""

    EXACT = "exact"  # Exact match
    PREFIX = "prefix"  # Prefix match
    PATTERN = "pattern"  # Regex pattern match


class Rule(BaseModel):
    """Rule for rate limiting."""

    path: str
    limit: int
    period: int = 60  # In seconds
    path_type: PathType = PathType.EXACT
    include_headers: bool = True
    group_by: Optional[str] = "ip"  # "ip", "user", or a custom header name

    def matches(self, request: Request) -> bool:
        """Check if rule matches request."""
        path = request.url.path

        if self.path_type == PathType.EXACT:
            return path == self.path
        elif self.path_type == PathType.PREFIX:
            return path.startswith(self.path)
        elif self.path_type == PathType.PATTERN:
            pattern = self.path.replace("*", ".*")
            return bool(re.match(f"^{pattern}$", path))

        return False

    def get_key(self, request: Request) -> str:
        """Get cache key for the request."""
        if self.group_by == "ip":
            client = request.client.host if request.client else "unknown"
        elif self.group_by == "user":
            # Assuming JWT or session-based auth with a user claim
            # This is just a placeholder - implement according to your auth system
            client = getattr(request.state, "user_id", "anonymous")
        else:
            # Use a custom header
            client = request.headers.get(self.group_by, "unknown")

        path_part = re.sub(r"[^a-zA-Z0-9]", "_", self.path)
        return f"ratelimit:{path_part}:{client}"


class BaseStorage(ABC):
    """Base storage for rate limiting."""

    @abstractmethod
    async def increment(self, key: str, period: int) -> int:
        """Increment counter for key and return current count."""
        pass

    @abstractmethod
    async def get_ttl(self, key: str) -> int:
        """Get TTL for key."""
        pass

    @abstractmethod
    async def reset(self, key: str) -> None:
        """Reset counter for key."""
        pass


class InMemoryStorage(BaseStorage):
    """In-memory storage for rate limiting."""

    def __init__(self):
        self._counters: Dict[str, int] = {}
        self._expiry: Dict[str, float] = {}
        self._lock = asyncio.Lock()

    async def increment(self, key: str, period: int) -> int:
        """Increment counter for key and return current count."""
        async with self._lock:
            now = time.time()

            # Check if key expired
            if key in self._expiry and now > self._expiry[key]:
                self._counters[key] = 0
                self._expiry[key] = now + period

            # Set initial values if key doesn't exist
            if key not in self._counters:
                self._counters[key] = 0
                self._expiry[key] = now + period

            # Increment counter
            self._counters[key] += 1
            return self._counters[key]

    async def get_ttl(self, key: str) -> int:
        """Get TTL for key."""
        if key not in self._expiry:
            return 0

        ttl = int(self._expiry[key] - time.time())
        return max(0, ttl)

    async def reset(self, key: str) -> None:
        """Reset counter for key."""
        async with self._lock:
            if key in self._counters:
                del self._counters[key]
            if key in self._expiry:
                del self._expiry[key]


class RedisStorage(BaseStorage):
    """Redis storage for rate limiting."""

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """Initialize Redis storage.

        Args:
            redis_url: Redis connection URL
        """
        self.redis = redis.from_url(redis_url)

    async def increment(self, key: str, period: int) -> int:
        """Increment counter for key and return current count.

        Args:
            key: The key to increment
            period: TTL period in seconds

        Returns:
            The new count after increment
        """
        try:
            async with self.redis.pipeline() as pipe:
                await pipe.incr(key)
                await pipe.expire(key, period)
                result = await pipe.execute()
                return result[0]  # Return the incremented value
        except redis.RedisError as e:
            print(f"Redis error during increment: {e}")
            return 0

    async def get_ttl(self, key: str) -> int:
        """Get TTL for key.

        Args:
            key: The key to check

        Returns:
            TTL in seconds, or 0 if key doesn't exist
        """
        try:
            ttl = await self.redis.ttl(key)
            return max(0, ttl)
        except redis.RedisError as e:
            print(f"Redis error during TTL check: {e}")
            return 0

    async def reset(self, key: str) -> None:
        """Reset counter for key.

        Args:
            key: The key to reset
        """
        try:
            await self.redis.delete(key)
        except redis.RedisError as e:
            print(f"Redis error during reset: {e}")


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware for rate limiting in FastAPI applications."""

    def __init__(
        self,
        app: ASGIApp,
        rules: List[Rule],
        storage: Optional[BaseStorage] = None,
        status_code: int = 429,
        exception_handler: Optional[Callable] = None,
    ):
        """
        Initialize rate limit middleware.

        Args:
            app: The ASGI application
            rules: List of rate limiting rules
            storage: Storage backend (defaults to InMemoryStorage)
            status_code: HTTP status code for rate limit exceeded
            exception_handler: Custom exception handler
        """
        super().__init__(app)
        self.rules = rules
        self.storage = storage or InMemoryStorage()
        self.status_code = status_code
        self.exception_handler = exception_handler

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process request through middleware."""
        # Skip OPTIONS requests (for CORS)
        if request.method == "OPTIONS":
            return await call_next(request)

        # Find matching rules
        matching_rules = [rule for rule in self.rules if rule.matches(request)]

        if not matching_rules:
            # No rule matches, skip rate limiting
            return await call_next(request)

        # Check each matching rule
        for rule in matching_rules:
            key = rule.get_key(request)

            # Increment counter for this key
            count = await self.storage.increment(key, rule.period)

            # If limit exceeded
            if count > rule.limit:
                # Get TTL for the key to calculate retry-after
                retry_after = await self.storage.get_ttl(key)

                # Use custom exception handler if provided
                if self.exception_handler:
                    return await self.exception_handler(
                        request, RateLimitExceeded(rule.limit, rule.period, retry_after)
                    )

                # Default response
                headers = {}
                if rule.include_headers:
                    headers = {
                        "X-RateLimit-Limit": str(rule.limit),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(retry_after),
                        "Retry-After": str(retry_after),
                    }

                return JSONResponse(
                    status_code=self.status_code,
                    content={
                        "detail": f"Rate limit exceeded: {rule.limit} requests per {rule.period} seconds",
                        "limit": rule.limit,
                        "period": rule.period,
                        "retry_after": retry_after,
                    },
                    headers=headers,
                )

            # Add rate limit headers to response if requested
            if rule.include_headers:
                request.state.rate_limit_info = {
                    "limit": rule.limit,
                    "current": count,
                    "remaining": max(0, rule.limit - count),
                    "reset": await self.storage.get_ttl(key),
                }

        # Process the request
        response = await call_next(request)

        # Add headers to response if applicable
        if hasattr(request.state, "rate_limit_info"):
            info = request.state.rate_limit_info
            response.headers["X-RateLimit-Limit"] = str(info["limit"])
            response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
            response.headers["X-RateLimit-Reset"] = str(info["reset"])

        return response
