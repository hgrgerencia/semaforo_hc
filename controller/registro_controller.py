
from config.bbdd_mongo import FactoryMongoDB

# categorias de productos a vender: BURGER, BEBIDAS, PLATAOS....
TABLE = "registro_obligaciones_hc"
SORT_COLLECTION = "nombre"

class registros_controller(FactoryMongoDB):
    pass

FactoryRegistros = registros_controller(TABLE, SORT_COLLECTION)

