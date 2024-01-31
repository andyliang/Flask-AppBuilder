from . import appbuilder

from .api.product_api import ProductModelApi,ProductRestApi

appbuilder.add_api(ProductModelApi)
appbuilder.add_api(ProductRestApi)