from flask import g
from flask_babel import lazy_gettext

from flask_appbuilder import ModelView
from flask_appbuilder.models.filters import BaseFilter
from flask_appbuilder.models.sqla.filters import get_field_setup_query
from flask_appbuilder.models.sqla.interface import SQLAInterface

from flask_appbuilder.security.registerviews import RegisterUserDBView

from ..model.sec import Company, Contact, ContactGroup
from ..sec_views import UserDBModelView

class FilterInManyFunction(BaseFilter):
    name = "Filter view where field is in a list returned by a function"

    def apply(self, query, func):
        query, field = get_field_setup_query(query, self.model, self.column_name)
        return query.filter(field.any(Company.id.in_(func())))


def get_user_companies():
    return set([company.id for company in g.user.companies])
    return g.user.companies


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)
    list_columns = [
        "name",
        "personal_celphone",
        "birthday",
        "contact_group.name",
        "created_by",
    ]
    add_columns = [
        "name",
        "address",
        "birthday",
        "personal_phone",
        "personal_celphone",
        "contact_group",
        "gender",
    ]
    edit_columns = [
        "name",
        "address",
        "birthday",
        "personal_phone",
        "personal_celphone",
        "contact_group",
        "gender",
    ]
    base_order = ("name", "asc")
    base_filters = [["created_by.companies", FilterInManyFunction, get_user_companies]]


class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]


class CompanyModelView(ModelView):
    datamodel = SQLAInterface(Company)
    list_columns = ["name", "MyUser"]
    related_views = [UserDBModelView]


class MyRegisterUserDBView(RegisterUserDBView):
    email_template = 'register_mail.html'
    email_subject = lazy_gettext('Your Account activation')
    activation_template = 'activation.html'
    form_title = lazy_gettext('Fill out the registration form')
    error_message = lazy_gettext('Not possible to register you at the moment, try again later')
    message = lazy_gettext('Registration sent to your email')
