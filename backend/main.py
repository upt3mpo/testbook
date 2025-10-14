import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from database import init_db
from logger import setup_logging
from routers import auth, dev, feed, posts, users

# Load environment variables from .env file
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
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
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)


# Request size limiting middleware
class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_upload_size: int = 10 * 1024 * 1024):  # 10MB default
        super().__init__(app)
        self.max_upload_size = max_upload_size

    async def dispatch(self, request: Request, call_next):
        if request.method in ["POST", "PUT", "PATCH"]:
            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > self.max_upload_size:
                return JSONResponse(status_code=413, content={"detail": "Request body too large"})
        return await call_next(request)


app.add_middleware(RequestSizeLimitMiddleware, max_upload_size=10 * 1024 * 1024)


# Health check endpoints (must be before static mounts)
@app.get("/api")
async def root():
    return {"message": "Welcome to Testbook API"}


@app.get("/api/health")
@limiter.limit("100/minute")
async def health_check(request: Request):
    """Health check endpoint with rate limiting headers"""
    return {"status": "healthy"}


# Include routers BEFORE static file mounts
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
app.include_router(feed.router, prefix="/api/feed", tags=["Feed"])
app.include_router(dev.router, prefix="/api/dev", tags=["Development"])

# Mount static files for images/videos
os.makedirs("static/images", exist_ok=True)
os.makedirs("static/videos", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve frontend in production (when frontend-dist exists)
# This must be LAST to not interfere with API routes
if os.path.exists("frontend-dist"):
    app.mount("/", StaticFiles(directory="frontend-dist", html=True), name="frontend")
