from flask_appbuilder import IndexView
from flask_appbuilder.baseviews import expose

class MyIndexView(IndexView):
    route_base = ""
    default_view = "index"
    index_template = "index.html"

    @expose("/")
    def index(self):
        self.update_redirect()
        return self.render_template(self.index_template, appbuilder=self.appbuilder)