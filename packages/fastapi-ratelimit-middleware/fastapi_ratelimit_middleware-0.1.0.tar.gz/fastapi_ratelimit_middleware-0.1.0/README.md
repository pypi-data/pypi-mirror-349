# FastAPI Rate Limit

A flexible rate limiting middleware for FastAPI applications.

## Features

- Simple and intuitive API
- Multiple storage backends (in-memory, Redis)
- Customizable rate limit rules
- Response headers with rate limit information
- Exception handling with customizable responses

## Installation

```bash
pip install fastapi-rate-limit
```

## Quick Start

```python
from fastapi import FastAPI
from fastapi_rate_limit import RateLimitMiddleware, Rule

app = FastAPI()

# Add rate limiting middleware
app.add_middleware(
    RateLimitMiddleware,
    rules=[
        Rule(path="/api/*", limit=10, period=60),  # 10 requests per minute for /api/* paths
    ]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/items")
async def get_items():
    return {"items": ["item1", "item2"]}
```

## Documentation

For more detailed documentation, please visit [our documentation](https://github.com/zaibe_.x/fastapi-rate-limit).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.