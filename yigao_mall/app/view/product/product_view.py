from flask_appbuilder.views import PublicFormView,ModelView,MasterDetailView
from flask_babel import lazy_gettext
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_appbuilder.models.sqla.interface import SQLAInterface
from ...model.system import SystemDict
from ...model.business_base_model import Category,CategorySecond,Product
from flask_appbuilder.exceptions import FABException
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder.models.sqla.filters import (FilterEqualFunction,FilterEqual,FilterInFunction)

from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget, BS3TextFieldWidget
from flask_appbuilder.widgets import ListThumbnail, ListBlock, ShowBlockWidget
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.baseviews import BaseCRUDView, BaseFormView, BaseView, expose, expose_api
from flask import (
    abort,
    flash,
    jsonify,
    make_response,
    redirect,
    request,
    send_file,
    session,
    url_for,
)

from ...widgets import ProductGridList
from ... import text,db
from ...tool.tools import get_user_id

class CategorySecondModelView(ModelView):
    datamodel = SQLAInterface(CategorySecond)
    list_columns = ['csname','category']

class CategoryModelView(ModelView):
    datamodel = SQLAInterface(Category)
    related_views = [CategorySecondModelView]

#用于管理自己的作品
class ProductModelView(ModelView):
    base_filters = [['uid', FilterEqualFunction, get_user_id]]
    datamodel = SQLAInterface(Product)

    base_order = ('pdate', 'desc')

    add_exclude_columns = ['myuser','pdate']

    list_columns = [
        "head_img_href_thumbnail",
        "pname",
        'old_price','new_price',
        "myuser",
    ]

#用户首页显示最新作品列表
class ProductGridModelView(ModelView):
    datamodel = SQLAInterface(Product)

    # lhz add param 实现对列表的返回按钮参数化，配置为True在列表头显示返回按钮
    list_back_btn = True

    show_title = '作品详情'

    base_permissions = ['can_list','can_show']

    list_columns = ['head_img_href','love_user_count','myuser','pname','old_price','new_price']
    label_columns = {'love_user_count':'喜欢的人','myuser':'作者','pname':'作品名称','old_price':'原价','new_price':'促销价'}

    show_columns = ['head_img_href','myuser','pname','old_price','new_price',
                    ]

    list_widget = ProductGridList

    # widget自定义切换
    # show_widget = ShowBlockWidget

    order_columns = ['click_count']

    show_template = 'product/show.html'

    @expose("/show/<pk>", methods=["GET"])
    @has_access
    def show(self, pk):
        # 查询产品分类信息
        ## 使用原生sql语句进行查询
        tmp_sql = """select cid,cname,group_concat(csid order by csid asc) csids,group_concat(csname order by csid asc) csnames
                                from (
                                         select c.id cid,cs.id csid,c.cname, cs.csname
                                         from category c,
                                              category_second cs
                                         where c.id = cs.cid
                                         order by c.id asc,cs.id asc
                                     ) tmp
                                group by cid
                                order by cid asc
                """

        query_sql = text(tmp_sql)
        result = db.session.query(text('cid'), text('cname'), text('csids'), text('csnames')).from_statement(
            query_sql).all()

        pk = self._deserialize_pk_if_composite(pk)
        widgets = self._show(pk)
        return self.render_template(
            self.show_template,
            pk=pk,
            title=self.show_title,
            widgets=widgets,
            related_views=self._related_views,
            category = result
        )









