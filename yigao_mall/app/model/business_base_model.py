from flask_appbuilder import Model
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Table,Float,Text
from sqlalchemy.orm import relationship,backref
import datetime

# 一级类别
class Category(Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    cname = Column(String(255), nullable=False)

    def __repr__(self):
        return self.cname

    def category_json(self):
        category_json = {}
        category_json["id"] = self.id
        category_json["cname"] = self.cname
        return category_json


# 二级类别
class CategorySecond(Model):
    __tablename__ = 'category_second'
    id = Column(Integer, primary_key=True)
    csname = Column(String(255), nullable=False)
    cid = Column(Integer, ForeignKey('category.id', ondelete='cascade'))
    category = relationship("Category", backref=backref('categoryseconds'))

    def __repr__(self):
        return self.csname

    def categorySecond_json(self):
        categorySecond_json = {}
        categorySecond_json["id"] = self.id
        categorySecond_json["csname"] = self.csname
        return categorySecond_json

# 作品
class Product(Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    pname = Column(String(255), nullable=False)
    old_price = Column(Float, nullable=False)
    new_price = Column(Float, nullable=False)
    images = Column(Text)
    pDesc = Column(Text)
    head_img = Column(Text)
    is_hot = Column(Integer, default=0)  # 0不是热卖品，1热卖品 2推广品
    is_sell = Column(Integer, default=1)  # 0销完 1在售
    is_pass = Column(Integer, default=0)  # 0正在审核 1审核未通过 2 审核通过
    pdate = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    click_count = Column(Integer, default=0)
    counts = Column(Integer, nullable=False)
    love_user = Column(Text)  # 喜爱的人
    uid = Column(Integer, ForeignKey("ab_user.id",ondelete='cascade'))
    myuser = relationship("MyUser", backref=backref('products', order_by=pdate.desc()))  #排序
    csid = Column(Integer, ForeignKey("category_second.id", ondelete='cascade'))
    category_second = relationship("CategorySecond", backref=backref("products", order_by=pdate.desc()))

    def __repr__(self):
        return self.pname

    def product_json(self):
        product_json = {}
        # product_json["pdate"] = self.pdate
        product_json["id"] = self.id
        product_json["pname"] = self.pname
        product_json["images"] = self.images.split('@')[0]
        product_json["head_img"] = self.head_img
        product_json["counts"] = self.counts
        product_json["old_price"] = self.old_price
        product_json["new_price"] = self.new_price
        return product_json

    def product_json2(self):
        product_json = {}
        product_json["pdate"] = self.pdate
        product_json["id"] = self.id
        product_json["pname"] = self.pname
        product_json["username"] = self.user.name
        return product_json

    def product_json1(self):
        product_json = {}
        product_json["id"] = self.id
        product_json["pname"] = self.pname
        product_json["images"] = self.images
        product_json["counts"] = self.counts
        product_json["old_price"] = self.old_price
        product_json["new_price"] = self.new_price
        product_json["pDesc"] = self.pDesc
        product_json["new_price"] = self.new_price
        return product_json


# 作品的交流评论
class Comment(Model):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    is_read = Column(Integer, default=0)  # 是否看过 0看过，1没有看过
    cdate = Column(DateTime, default=datetime.datetime.now)
    uid = Column(Integer, ForeignKey("ab_user.id", ondelete='cascade'))
    myuser = relationship("MyUser", backref=backref('commments', order_by=cdate.desc()))
    comment_id = Column(Integer, ForeignKey('comment.id'))
    comment_parent = relationship("Comment", backref=backref("comments"), remote_side=[id])
    pid = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", backref=backref('commments', order_by=cdate.desc()))


# 购物车
class ShopCart(Model):
    __tablename__ = "shop_cart"
    id = Column(Integer, primary_key=True)
    sdate = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    count = Column(Integer,default=0)
    sub_total = Column(Float,default=0)
    uid = Column(Integer, ForeignKey("ab_user.id", ondelete='cascade'))
    myuser = relationship("MyUser", backref=backref("shopcarts", order_by=sdate.desc()))
    pid = Column(Integer, ForeignKey("product.id"))
    product = relationship('Product', backref=backref("shopcarts"))


# 订单
class Order(Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    total_money = Column(Float,default=0)
    ordertime = Column(DateTime, default=datetime.datetime.now)
    state = Column(Integer, default=0)  # 0未支付，1送达中 2送达完毕
    name = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addr = Column(String(255), nullable=False)
    uid = Column(Integer, ForeignKey("ab_user.id", ondelete='cascade'))
    myuser = relationship("MyUser", backref=backref("orders", order_by=ordertime.desc()))
    order_last_time = Column(String(50))


# 订单项
class OrderItem(Model):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False, default=0)
    sub_total = Column(Float, nullable=False, default=0)
    pid = Column(Integer, ForeignKey("product.id", ondelete='cascade'))
    product = relationship("Product", backref=backref("orderItems"))
    oid = Column(Integer, ForeignKey("order.id", ondelete='cascade'))
    order = relationship("Order", backref=backref("orderItems"))