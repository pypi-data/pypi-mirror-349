import inspect

from typing import Any, Type

from dependency_injector import containers, providers
from fastapi import APIRouter


class BaseFlavor:
    """Base class for creating API flavors that handle routing and endpoint registration.

    A flavor is a collection of related endpoints grouped under a common prefix and tags.
    """

    def __init__(
        self,
        name: str = "",
        prefix: str = "",
        tags: list[str] = [],
        services: dict[str, Type] = {},
    ):
        """Initialize a new flavor instance."""
        self.name = name
        self.prefix = prefix
        self.tags = tags
        self.services = services

        self.router = APIRouter(tags=self.tags, prefix=self.prefix)
        self.container = containers.DynamicContainer()

        for name, service in self.services.items():
            setattr(self.container, name, providers.Singleton(service))
            setattr(self, name, getattr(self.container, name)())

        self._router_from_controller()

    def _router_from_controller(self, **defaults_route_args: Any) -> None:
        """Build a router from a controller instance annotated endpoints).

        Args:
        ----
            defaults_route_args: Default arguments to pass to all routes

        Raises:
        ------
            ValueError: If no endpoints are found in the controller

        """
        # Find all methods that have endpoint definitions attached
        members = inspect.getmembers(
            self, lambda x: hasattr(x, "__endpoint_definitions__")
        )

        # Register each endpoint with the router
        for _, endpoint in members:
            for endpoint_definition in getattr(endpoint, "__endpoint_definitions__"):
                kwargs = {**defaults_route_args, **endpoint_definition.kwargs}

                self.router.add_api_route(
                    endpoint_definition.path,
                    endpoint,
                    methods=[endpoint_definition.method],
                    **kwargs,
                )
