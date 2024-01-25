from time import strftime

from flask_appbuilder import Model,CompactCRUDMixin
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, Integer, String,Sequence
from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
import datetime


class Comp(Model):
    __tablename__ = 'comp'
    id = Column(Integer,Sequence('comp_seq'),primary_key=True,comment='主键',autoincrement=True)
    comp_name = Column(String(200),nullable=False,comment='企业名称')
    comp_licence = Column(String(200),comment='企业经营许可证号',unique=True)
    comp_address = Column(String(2000),comment='企业地址')
    remark = Column(String(2000), comment='备注')
    comp_type_id = Column(Integer, ForeignKey("system_dict.id"), nullable=False)
    comp_type = relationship(
        "SystemDict",
        primaryjoin="and_(Comp.comp_type_id==SystemDict.id)",
    )
    reg_date = Column(Date,comment='注册日期')
    # comp_myusers = relationship('MyUser', backref='userscomp') #此条加上会影响主次视图

    #关联tags,#此条加上会影响主次视图，另外，关联显示存在问题
    # tags = relationship(
    #     "Tag",
    #     secondary=assoc_comp_tag,
    #     backref="comp",
    #     info={"required": False} #是否必填
    # )
    #comp_vhcls = relationship('Vhcl', backref='vhcl_comp_ref') #此条加上会影响主次视图

    def __repr__(self):
        return self.comp_name

assoc_user_company = Table(
    "ab_user_company",
    Model.metadata,
    Column("id", Integer, primary_key=True),
    Column("company_id", Integer, ForeignKey("company.id")),
    Column("myuser_id", Integer, ForeignKey("ab_user.id")),
)

#用户扩展，需要手工创建自动和外键
class MyUser(User):
    __tablename__ = "ab_user"
    mobile = Column(String(20))
    address = Column(String(200))
    comp_id_fk = Column(Integer, ForeignKey("comp.id"), nullable=True)
    comp = relationship("Comp")
    order_no = Column(Integer, comment='排序')
    emp_number = Column(String(150))
    companies = relationship("Company", secondary=assoc_user_company, backref="MyUser")

class UserDepartment(Model):
    __tablename__ = "ab_user_department"
    id = Column(Integer, Sequence('ab_user_department_seq'), primary_key=True, comment='主键', autoincrement=True)
    user_id = Column(Integer, nullable=False)
    department_id = Column(Integer, nullable=False)
    start_work_date = Column(DateTime, comment='开始工作时间')
    end_work_date = Column(DateTime, comment='结束工作时间')
    status = Column(Integer, nullable=False, comment='1:有效，0：失效')
    remark = Column(String(200), comment='备注')

class SystemLog(AuditMixin,Model):
    __tablename__ = 'system_log'
    id = Column(Integer,Sequence('system_log_seq'),primary_key=True,comment='主键',autoincrement=True)
    module_name = Column(String(200),nullable=False,comment='模块名称')
    action_name = Column(String(200),nullable=False,comment='事件名称')
    action_remark = Column(String(2000),comment='事件备注')
    object_id = Column(Integer,nullable=False,comment='对象ID')

class SystemDict(AuditMixin,Model):
    __tablename__ = 'system_dict'
    id = Column(Integer, Sequence('system_dict_seq'), primary_key=True, comment='主键', autoincrement=True)
    type = Column(String(100), nullable=False, comment='参数类型')
    type_name = Column(String(100), nullable=False, comment='参数名称')
    code = Column(String(100), nullable=False, comment='参数值')
    name = Column(String(200), comment='参数名称')
    orders = Column(Integer, comment='显示顺序')
    remark = Column(String(200), comment='备注')

    def __repr__(self):
        return self.name

class SystemDictComponent(AuditMixin,Model):
    __tablename__ = 'system_dict_component'
    id = Column(Integer, Sequence('system_dict_component_seq'), primary_key=True, comment='主键', autoincrement=True)
    type = Column(String(100), nullable=False, comment='参数类型')
    type_name = Column(String(100), nullable=False, comment='参数名称')
    code = Column(String(100), nullable=False, comment='参数值')
    name = Column(String(200), comment='参数名称')
    orders = Column(Integer, comment='显示顺序')
    remark = Column(String(200), comment='备注')

    def __repr__(self):
        return self.name

class SystemDictRole(AuditMixin,Model):
    __tablename__ = 'system_dict_role'
    id = Column(Integer, Sequence('system_dict_role_seq'), primary_key=True, comment='主键', autoincrement=True)
    type = Column(String(100), nullable=False, comment='参数类型')
    type_name = Column(String(100), nullable=False, comment='参数名称')
    code = Column(String(100), nullable=False, comment='参数值')
    name = Column(String(200), comment='参数名称')
    orders = Column(Integer, comment='显示顺序')
    remark = Column(String(200), comment='备注')

    def __repr__(self):
        return self.name


class SysArea(Model):
    __tablename__ = 'sys_area'
    id = Column(Integer, Sequence('sys_area_seq'),primary_key=True, comment='主键', autoincrement=True)
    super_id = Column(Integer, comment='上级ID')
    type = Column(String(20), comment='地区类型')
    code = Column(String(20), comment='识别代码')
    name_en = Column(String(50), comment='英文名称')
    name_cn = Column(String(50), comment='中文名称')
    zip_code = Column(String(50), comment='邮编')
    zone = Column(String(20), comment='分区')
    remark = Column(String(200), comment='备注')
    create_datetime = Column(DateTime, default=datetime.datetime.now(), comment='创建时间')
    create_user = Column(Integer, comment='创建人')
    change_datetime = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now(),comment='变更时间')
    change_user = Column(Integer, comment='变更人')

    def __repr__(self):
        return self.code + '(' + self.name_cn + ')'

class Calendar(Model):
    __tablename__ = "calendar"
    id = Column(Integer, Sequence('calendar_seq'), primary_key=True, comment='主键', autoincrement=True)
    day = Column(Date, comment='日期')
    week = Column(Integer, comment='所属周')
    week_day = Column(Integer, comment='星期')
    working_day = Column(Integer, comment='是否上班')
    holiday = Column(String(30), comment='节假日名称')
    status = Column(Integer, comment='1:有效，0：失效')
    remark = Column(String(200), comment='备注')
    create_datetime =  Column(DateTime, comment='创建时间')
    create_id = Column(String(50), comment='创建人')
    update_datetime =  Column(DateTime, comment='修改时间')
    update_id = Column(String(50), comment='修改人')

    def __repr__(self):
        date = self.day
        return str(date.year)+'-'+str(date.month)+'-'+str(date.day)

    # todo 未生效
    def week_day_show(self):
        weak_day = self.week_day
        week_day_str = '星期'
        if weak_day == 1:
            week_day_str = week_day_str + '一'
        elif weak_day == 2:
            week_day_str = week_day_str + '二'
        elif weak_day == 3:
            week_day_str = week_day_str + '三'
        elif weak_day == 4:
            week_day_str = week_day_str + '四'
        elif weak_day == 5:
            week_day_str = week_day_str + '五'
        elif weak_day == 6:
            week_day_str = week_day_str + '六'
        elif weak_day == 7:
            week_day_str = week_day_str + '日'
        return week_day_str


