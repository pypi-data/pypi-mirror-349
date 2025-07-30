from typing import Any, Dict, Optional, Sequence, Tuple

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .middlewares import runtime, http_exception, validation_exception
from .routes.router import Router


__all__ = ("Application",)


class Application:
    """
    Wrapper for configuring a FastAPI application using SOLID and clean OOP structure.
    """

    def __init__(
        self,
        title: str,
        version: str = "*",
        redoc_url: Optional[str] = None,
        docs_url: Optional[str] = None,
        applications: Optional[Sequence[Tuple[str, "Application"]]] = None,
        routers: Optional[Sequence[Tuple[str, Router]]] = None,
        gzip_min_size: Optional[int] = None,
        session_middleware_settings: Optional[Dict[str, Any]] = None,
        middlewares: Optional[Sequence[Any]] = None,
        lifespan: Optional[Any] = None,
        redirect_root_to: Optional[str] = None,
        cors_settings: Optional[Dict[str, Any]] = None,
    ) -> None:
        # Core metadata
        self.title = title
        self.version = version
        self.redoc_url = redoc_url
        self.docs_url = docs_url
        self.lifespan = lifespan
        self.redirect_root_to = redirect_root_to

        # Sub-apps and routers
        self.applications = applications or ()
        self.routers = routers or ()

        # Middleware configuration
        self.middlewares = (runtime.Runtime(), *(middlewares or ()))
        self.gzip_min_size = gzip_min_size
        self.session_settings = session_middleware_settings or {}

        # CORS defaults and overrides
        self.cors_settings: Dict[str, Any] = {
            "allow_origins": ["*"],
            "allow_credentials": True,
            "allow_methods": ["*"],
            "allow_headers": ["*"],
            "expose_headers": [],
            "allow_origin_regex": None,
            "max_age": 600,
        }
        if cors_settings:
            self.cors_settings.update(cors_settings)

        # Build the FastAPI instance
        self.app = self._create_app()

    def _create_app(self) -> FastAPI:
        app = FastAPI(
            title=self.title,
            version=self.version,
            redoc_url=self.redoc_url,
            docs_url=self.docs_url,
            swagger_ui_parameters={"defaultModelsExpandDepth": -1},
            lifespan=self.lifespan,
        )
        self._configure_gzip(app)
        self._configure_session(app)
        self._configure_middlewares(app)
        self._configure_cors(app)
        self._configure_exception_handlers(app)
        self._mount_sub_applications(app)
        self._include_routers(app)
        self._configure_root_redirect(app)
        return app

    def _configure_gzip(self, app: FastAPI) -> None:
        if self.gzip_min_size is not None:
            from fastapi.middleware.gzip import GZipMiddleware
            app.add_middleware(GZipMiddleware, minimum_size=self.gzip_min_size)

    def _configure_session(self, app: FastAPI) -> None:
        if self.session_settings:
            from starlette.middleware.sessions import SessionMiddleware
            app.add_middleware(SessionMiddleware, **self.session_settings)

    def _configure_middlewares(self, app: FastAPI) -> None:
        if self.middlewares:
            from starlette.middleware.base import BaseHTTPMiddleware

            for mw in self.middlewares:
                app.add_middleware(BaseHTTPMiddleware, dispatch=mw)

    def _configure_cors(self, app: FastAPI) -> None:
        if self.cors_settings:
            from fastapi.middleware.cors import CORSMiddleware
            app.add_middleware(CORSMiddleware, **self.cors_settings)

    def _configure_exception_handlers(self, app: FastAPI) -> None:
        from starlette.exceptions import HTTPException as StarletteHTTPException
        @app.exception_handler(StarletteHTTPException)
        async def _http_exception_handler(request, exc):
            return await http_exception.http_exception_handler(request, exc)

        from fastapi.exceptions import RequestValidationError
        @app.exception_handler(RequestValidationError)
        async def _validation_exception_handler(request, exc):
            return await validation_exception.validation_exception_handler(request, exc)

    def _mount_sub_applications(self, app: FastAPI) -> None:
        for prefix, sub_app in self.applications:
            app.mount(prefix, sub_app.get_app())

    def _include_routers(self, app: FastAPI) -> None:
        for prefix, router in self.routers:
            app.include_router(
                router=router.get_router(),
                prefix=prefix,
            )

    def _configure_root_redirect(self, app: FastAPI) -> None:
        if self.redirect_root_to:
            @app.get("/", include_in_schema=False)
            async def _redirect():
                return RedirectResponse(self.redirect_root_to)

    def get_app(self) -> FastAPI:
        """Return the fully configured FastAPI application."""
        return self.app
