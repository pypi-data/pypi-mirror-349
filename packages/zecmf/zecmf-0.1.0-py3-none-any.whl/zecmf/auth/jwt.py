"""JWT authentication module for micro-framework."""

from collections.abc import Callable
from typing import Any, TypeVar

from flask import Flask, Response, current_app, g, request
from flask_jwt_extended import (
    JWTManager,
    get_jwt,
    get_jwt_identity,
    verify_jwt_in_request,
)
from werkzeug.exceptions import Unauthorized

# Type variable for generic functions
F = TypeVar("F", bound=Callable[..., Any])


jwt = JWTManager()


def _check_public_endpoint(endpoint_func: Callable[..., Any]) -> bool:
    """Check if an endpoint is marked as public."""
    # Check if it's a class-based view (like Flask-RESTX resources)
    if hasattr(endpoint_func, "view_class"):
        view_class = endpoint_func.view_class

        # Check class for the is_public attribute
        if hasattr(view_class, "is_public") and view_class.is_public:
            return True

        # Check the specific method for the is_public attribute
        method = request.method.lower()
        if hasattr(view_class, method):
            handler = getattr(view_class, method)
            if hasattr(handler, "is_public") and handler.is_public:
                return True

    # For regular function-based views
    elif hasattr(endpoint_func, "is_public") and endpoint_func.is_public:
        return True

    return False


def _authenticate_request() -> None:
    """Authenticate the current request using JWT."""
    try:
        verify_jwt_in_request()

        # Get JWT claims
        claims = get_jwt()
        user_roles = claims.get("roles", [])

        # Store user info in flask g object for use in the request
        g.user_id = get_jwt_identity()
        g.user_roles = user_roles
    except Exception as err:
        raise Unauthorized("Authentication required") from err


def init_jwt(app: Flask) -> None:
    """Initialize JWT manager with the Flask app."""
    jwt.init_app(app)

    # Register before_request handler to enforce authentication by default
    @app.before_request
    def enforce_authentication() -> Response | None:
        """Enforce authentication for each request unless marked as public."""
        # Skip OPTIONS requests for CORS support
        if request.method == "OPTIONS":
            return None

        # Allow access to swagger.json only in debug mode
        if app.debug and request.path.endswith("/swagger.json"):
            return None

        # Check if the endpoint is public
        if request.endpoint is not None:
            endpoint_func = current_app.view_functions.get(request.endpoint)
            if endpoint_func is not None and _check_public_endpoint(endpoint_func):
                return None

        # If we're here, authentication is required
        _authenticate_request()
        return None
