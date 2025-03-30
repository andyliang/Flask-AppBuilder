from flask import render_template

from . import appbuilder

from .view.sec_user import CompanyModelView,GroupModelView,ContactModelView,MyRegisterUserDBView
from .view.product.product_view import ProductModelView,CategoryModelView,CategorySecondModelView,ProductGridModelView

appbuilder.add_view(CompanyModelView, "Companys", icon="fa-folder-open-o")
appbuilder.add_view(GroupModelView,"List Groups",icon="fa-folder-open-o",category="Contacts",category_icon="fa-envelope",)
appbuilder.add_view(ContactModelView, "List Contacts", icon="fa-envelope", category="Contacts")
appbuilder.add_view(CategoryModelView, "分类", icon="fa-folder-open-o",category="作品管理")
appbuilder.add_view(CategorySecondModelView, "二级分类", icon="fa-folder-open-o",category="作品管理")
appbuilder.add_view(ProductModelView, "我的作品", icon="fa-folder-open-o",category="作品管理")

appbuilder.add_view_no_menu(ProductGridModelView)


# appbuilder.add_view(
#     MyRegisterUserDBView, "REGISTER", icon="fa-envelope", category="Contacts"
# )

"""
    Create your Model based REST API::
    
    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::

    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::

    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""

"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html", base_template=appbuilder.base_template, appbuilder=appbuilder
        ),
        404,
    )
