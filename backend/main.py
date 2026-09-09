import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response
from starlette.types import ASGIApp

from database import init_db
from logger import setup_logging
from routers import auth, dev, feed, posts, users

# Load environment variables from .env file
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    # FastAPI's lifespan protocol requires this parameter even though
    # this function doesn't need it.
    # Initialize logging on startup
    setup_logging()

    # Initialize database on startup
    init_db()
    yield


# Initialize rate limiter based on environment
# In testing mode, use much higher limits to avoid test interference
TESTING_MODE = os.getenv("TESTING", "false").lower() == "true"

if TESTING_MODE:
    # Testing mode: Very high limits to avoid test failures
    limiter = Limiter(key_func=get_remote_address, default_limits=["1000/minute"])
else:
    # Production mode: Reasonable limits for security
    limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(
    title="Testbook API",
    description="A social media API for testing purposes",
    version="1.0.0",
    lifespan=lifespan,
)

# Add rate limiter to app state
app.state.limiter = limiter
# slowapi's handler is typed for the specific RateLimitExceeded subclass,
# not the generic Exception Starlette's stub expects - safe at runtime
# (FastAPI only calls it for that exact registered exception type), but
# mypy's parameter contravariance check can't see that.
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

# CORS middleware
#
# allow_origins=["*"] means any site can call this API from a browser. That's
# appropriate for a local learning environment where "the frontend" could be
# running on any port a student happens to pick, and there's nothing behind
# this API worth protecting from a random third-party site. A real
# deployment should replace it with the specific origin(s) the real frontend
# is served from.
#
# allow_credentials is deliberately False, not True: this app authenticates
# with a bearer token in the Authorization header (see auth.py), stored in
# localStorage, never a cookie - confirmed no code anywhere sets a cookie or
# sends `credentials: include`/`withCredentials`. CORS "credentials" means
# cookies, TLS client certs, and HTTP auth, not a bearer token in a custom
# header, so this app was never using it. Leaving it True while allow_origins
# is a wildcard would have been a strictly worse combination for no benefit:
# browsers refuse a literal `*` alongside credentials, so CORS middleware
# implementations (Starlette's included) special-case it by reflecting
# whatever Origin the request actually sent - meaning any origin, not just
# a wildcard, would have been allowed to make credentialed requests, if this
# app ever started using cookies without someone revisiting this setting.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)


# Request size limiting middleware
class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, max_upload_size: int = 10 * 1024 * 1024
    ) -> None:  # 10MB default
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.method in ["POST", "PUT", "PATCH"]:
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > self.max_upload_size:
                return JSONResponse(
                    status_code=413, content={"detail": "Request body too large"}
                )
        return await call_next(request)


app.add_middleware(RequestSizeLimitMiddleware, max_upload_size=10 * 1024 * 1024)


# Health check endpoints (must be before static mounts)
@app.get("/api")
async def root() -> dict[str, str]:
    return {"message": "Welcome to Testbook API"}


@app.get("/api/health")
@limiter.limit("100/minute")
async def health_check(request: Request) -> dict[str, str]:  # noqa: ARG001
    """Health check endpoint with rate limiting headers.

    request is unused in the body but required: slowapi's @limiter.limit
    reads the client's address off it to enforce the rate limit.
    """
    return {"status": "healthy"}


# Include routers BEFORE static file mounts
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
app.include_router(feed.router, prefix="/api/feed", tags=["Feed"])
app.include_router(dev.router, prefix="/api/dev", tags=["Development"])

# Mount static files for images/videos
Path("static/images").mkdir(parents=True, exist_ok=True)
Path("static/videos").mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve frontend in production (when frontend-dist exists)
# This must be LAST to not interfere with API routes
if Path("frontend-dist").exists():
    app.mount("/", StaticFiles(directory="frontend-dist", html=True), name="frontend")
