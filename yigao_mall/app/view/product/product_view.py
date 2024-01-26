from flask_appbuilder.views import PublicFormView,ModelView,MasterDetailView
from flask_babel import lazy_gettext
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_appbuilder.models.sqla.interface import SQLAInterface
from ...model.system import SystemDict
from ...model.business_base_model import Category,CategorySecond,Product
from flask_appbuilder.exceptions import FABException

from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget, BS3TextFieldWidget
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

class CategorySecondModelView(ModelView):
    datamodel = SQLAInterface(CategorySecond)
    list_columns = ['csname','category']

class CategoryModelView(ModelView):
    datamodel = SQLAInterface(Category)
    related_views = [CategorySecondModelView]

class ProductModelView(ModelView):
    datamodel = SQLAInterface(Product)


