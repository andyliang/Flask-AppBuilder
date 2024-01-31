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

    @expose('/love_this_product', methods=['POST'])
    @protect(allow_browser_login=True)
    def love_this_product(self):
        ids = json.loads(request.data)['ids']
        try:
            delete_sql = "update department set status=-1,change_datetime='" + now_str + "'" + " where id in (%s)" % ids
            db.session.execute(delete_sql)
            db.session.commit()
            resp = dict()
            resp["msg"] = "删除成功！"
            # resp["code1"] = 200  #由于响应本身具有status状态，因此这个code字段可以不填
            return self.response(200, **resp)
        except Exception as e:
            db.session.rollback()
            resp = dict()
            resp["msg"] = "删除出现异常:" + str(e)
            resp["code1"] = 500  # 由于响应500状态，因此这个code1字段需要填写
            return self.response(200, **resp)