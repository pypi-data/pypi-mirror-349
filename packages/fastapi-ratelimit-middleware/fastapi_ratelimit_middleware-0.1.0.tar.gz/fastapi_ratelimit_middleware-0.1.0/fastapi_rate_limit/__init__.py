"""
FastAPI Rate Limit - Rate limiting middleware for FastAPI applications.
"""

__version__ = "0.1.0"

from fastapi_rate_limit.middleware import RateLimitMiddleware, Rule, RateLimitExceeded

__all__ = ["RateLimitMiddleware", "Rule", "RateLimitExceeded"]
