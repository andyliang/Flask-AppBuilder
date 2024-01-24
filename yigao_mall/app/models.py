from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

#1、自定义模型，导入模型后，系统会自动初始化不存在的表
#系统日志及字典
from .model.system import Comp,MyUser,SystemLog,SystemDict,UserDepartment,SystemDictComponent,SystemDictRole
from .model.sec import Company, Contact, ContactGroup

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
