from flask_appbuilder.widgets import ListWidget

class CategoryDivList(ListWidget):
    template = "product/category_div_list_widget.html"

class ProductGridList(ListWidget):
    template = "product/product_grid_list_widget.html"
