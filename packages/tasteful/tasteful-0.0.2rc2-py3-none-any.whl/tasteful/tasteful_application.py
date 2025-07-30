from typing import List, Type

from dependency_injector import providers
from fastapi import FastAPI, Security

from tasteful.base_flavor import BaseFlavor
from tasteful.containers.tasteful_container import TastefulContainer


class TastefulApp:
    def __init__(
        self,
        title: str,
        version: str,
        flavors: List[Type[BaseFlavor]],
        authentication_backends: list[Security],
    ):
        self.app = FastAPI(
            title=title, version=version, dependencies=authentication_backends
        )
        self.container = TastefulContainer()
        self.app.container = self.container
        self.flavors = flavors

        self.register_flavors()

    def register_flavors(
        self,
    ) -> None:
        """Register all flavors with the app."""
        # Create a instance of all flavor at runtime by using an AbstractFactory
        for flavor in self.flavors:
            self.container.flavor_factory.override(
                providers.Factory(
                    flavor,
                    name=flavor.name,
                    prefix=flavor.prefix,
                    tags=flavor.tags,
                    services=flavor.services,
                )
            )
            injected_flavor = self.container.flavor_factory()
            self.app.include_router(injected_flavor.router)
