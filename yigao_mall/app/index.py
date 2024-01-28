from flask_appbuilder import IndexView
from flask_appbuilder.baseviews import expose
from . import db
from . import text
from .view.product.product_view import ProductGridModelView

class MyIndexView(IndexView):
    route_base = ""
    default_view = "index"
    index_template = "index.html"

    @expose("/")
    def index(self):
        #查询产品分类信息
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
        result = db.session.query(text('cid'),text('cname'),text('csids'),text('csnames')).from_statement(query_sql).all()

        #查询产品信息
        product_view = ProductGridModelView()

        self.update_redirect()
        return self.render_template(self.index_template, appbuilder=self.appbuilder,
                                    category = result,
                                    widgets = product_view._list())

