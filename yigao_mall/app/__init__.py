import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.menu import Menu
#from flask_migrate import Migrate
from flask_cors import CORS
from .sec import MySecurityManager

"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
CORS(app, supports_credentials=True) #lhz add support cors
app.config.from_object("config")
db = SQLA(app)

#lhz add
# migrate = Migrate(app,db,render_as_batch=True)


#原默认方法
# appbuilder = AppBuilder(app, db.session)

#重新改变初始化首页
from .index import MyIndexView
appbuilder = AppBuilder(app, db.session, security_manager_class=MySecurityManager,indexview=MyIndexView,menu=Menu(reverse=True),base_template='mybase.html')

"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

from . import models
from . import views
# from . import apis

#2、创建所有model到数据库
db.create_all()

# 全文检索数据库
'''
import flask_whooshalchemy as whooshalchemy
from app.model.requirement_model import Requirement,Post
whooshalchemy.whoosh_index(app, Post)
whooshalchemy.whoosh_index(app, Requirement)
'''