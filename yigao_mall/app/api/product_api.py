from flask_appbuilder import ModelRestApi, BaseView, has_access, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from ..model.business_base_model import Product

class ProductModelApi(ModelRestApi):
    resource_name = "product_api"  #访问方式：/api/v1/product_api/
    datamodel = SQLAInterface(Product)
    allow_browser_login = True
    list_columns = ["pname", "old_price"]
    show_columns = [
            "pname",
            "old_price"]