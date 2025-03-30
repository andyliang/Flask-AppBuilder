from flask import request
from flask_appbuilder import ModelRestApi, BaseView, has_access, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from ..model.business_base_model import Product
from flask_appbuilder.models.filters import BaseFilter
from sqlalchemy import or_,text
from flask_appbuilder.api import BaseApi, expose, rison, safe
from flask_appbuilder.security.decorators import protect
from .. import db

class ProductModelApi(ModelRestApi):
    resource_name = "product_api"  #访问方式：/api/v1/product_api/
    datamodel = SQLAInterface(Product)
    allow_browser_login = True
    list_columns = ["pname", "old_price"]
    show_columns = [
            "pname",
            "old_price"]

class ProductRestApi(BaseApi):
    resource_name = 'productrestapi' #注意资源名要用小写

    @expose('/love_this_product/<string:pk>', methods=['POST'])
    @protect(allow_browser_login=True)
    def love_this_product(self,pk):
        tmp = pk
        try:
            # 查询当前用户是否在喜欢的人列表中


            delete_sql = "update department set status=-1,change_datetime='" + now_str + "'" + " where id in (%s)" % ids
            db.session.execute(delete_sql)
            db.session.commit()

            resp = dict()
            resp["result_code"] = 0
            resp["message"] = "success"
            resp["result"] = {
                "data": 0,
            }
            return self.response(200, **resp)

        except Exception as e:
            db.session.rollback()
            resp = dict()
            resp["result_code"] = -1
            resp["message"] = "failed"
            resp["result"] = {
                "data": str(e),
            }
            return self.response(200, **resp)