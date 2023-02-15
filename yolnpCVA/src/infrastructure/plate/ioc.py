import inject
from src.domain.plate.interface.PlateInterface import PlateInterface
from src.infrastructure.plate.repository import MongoDBPlateRepository


def ioc_config(binder):
    binder.bind(PlateInterface, MongoDBPlateRepository())

def register_ioc():
    inject.configure(ioc_config)


"""

When you need use the config, then:

from src.infrastructure.plate.ioc import register_ioc

register_ioc()

"""