from dependency_injector import containers, providers
from tasteful.base_flavor import BaseFlavor


class TastefulContainer(containers.DeclarativeContainer):
    # Flavors related
    flavor_factory = providers.AbstractFactory(BaseFlavor)
