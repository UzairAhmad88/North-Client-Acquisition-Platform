import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.v1.router import router as api_v1_router
from app.core.config import settings
from app.core.database import check_db_health
from app.core.exceptions import AppError
from app.core.logging import configure_logging
from app.core.middleware import RequestIdMiddleware, RequestLoggingMiddleware

configure_logging()
logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.app_name} v{settings.app_version} ({settings.app_env})")
    yield
    logger.info(f"Shutting down {settings.app_name}")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestIdMiddleware)


# Exception Handlers
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "RESOURCE_NOT_FOUND",
                "message": "Resource not found",
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", None)
    code_map = {
        401: "AUTH_REQUIRED",
        403: "FORBIDDEN",
        404: "RESOURCE_NOT_FOUND",
        409: "CONFLICT",
        429: "RATE_LIMITED",
    }
    code = code_map.get(exc.status_code, "HTTP_ERROR")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": code,
                "message": str(exc.detail),
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", None)
    errs = exc.errors()
    default_msg = "Invalid request body or parameters"
    message = errs[0].get("msg", default_msg) if errs else "Validation error"
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": message,
                "request_id": request_id,
            }
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    logger.exception(f"Unhandled exception on [{request_id}]: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "request_id": request_id,
            }
        },
    )


# Health Check Endpoints
@app.get("/health")
def health():
    return {"data": {"status": "ok", "app": settings.app_name, "version": settings.app_version}}


@app.get("/health/live")
def live():
    return {"data": {"status": "alive"}}


@app.get("/health/ready")
def ready(db: Session = Depends(get_db)):
    db_healthy = check_db_health(db)
    if db_healthy:
        return {"data": {"status": "ready", "database": "connected"}}
    return JSONResponse(
        status_code=503,
        content={"data": {"status": "degraded", "database": "disconnected"}},
    )


@app.get("/health/deep")
def deep_health():
    from app.reliability.health import DeepHealthEngine
    engine = DeepHealthEngine()
    result = engine.run_all_checks()
    return {"data": result.to_dict()}


# Mount API V1 Router
app.include_router(api_v1_router, prefix=settings.api_v1_prefix)
