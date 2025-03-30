from flask import g
from ..models import MyUser,Calendar
from .. import db
from sqlalchemy.sql import text

def get_user_id():
    return g.user.id

def get_user_comp():
    return g.user.comp

def get_user_comp_id():
    return g.user.comp_id_fk

def get_search_users():
    users = []
    if_super_admin = False
    if_admin = False
    for user_role in g.user.roles:
        if 'Admin' in user_role.name:
            if_super_admin = True
            break
        if '管理员' in user_role.name:
            if_admin = True
            break
    if if_super_admin: #超级管理员时需要所有
        # 遍历所有用户
        all_users = db.session.query(MyUser).all()
        for each_user in all_users:
            users.append(each_user.id)
    elif if_admin: #管理员时，则获取该企业的所有用户
        for each_user in g.user.comp.comp_myusers:
            users.append(each_user.id)
    else: #非管理员时，则仅当前用户
        users.append(g.user.id)
    return users

def get_workingdaynum_by_start_end(start_date,end_date):
    query_sql = text("""select count(*) as num from calendar where working_day=1
                                    and day >= strftime('%Y-%m-%d',:start_date)
                                    and day <= strftime('%Y-%m-%d',:end_date)
                                        """)
    result = db.session.query('num').from_statement(query_sql) \
        .params(start_date=start_date, end_date=end_date) \
        .first()[0]
    if result:
        return result
    else:
        return 0

def get_workingday_ids_by_start_end(start_date,end_date):
    query_sql = text("""select id as id from calendar where working_day=1
                                    and day >= strftime('%Y-%m-%d',:start_date)
                                    and day <= strftime('%Y-%m-%d',:end_date)
                                    order by day asc
                                        """)
    result = db.session.query('id').from_statement(query_sql) \
        .params(start_date=start_date, end_date=end_date) \
        .all()
    if result:
        return result
    else:
        return []

def is_working_day(date_str):
    '''YYYY-MM-DD是否工作日'''
    query_sql = text("""select count(*) as total from calendar where working_day=1
                                    and day == strftime('%Y-%m-%d',:date_str)
                                        """)
    result = db.session.query('total').from_statement(query_sql) \
        .params(date_str=date_str).first()[0]
    if result > 0:
        return True
    else:
        return False