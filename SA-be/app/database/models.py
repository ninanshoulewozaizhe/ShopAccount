from app.database import db
from sqlalchemy.inspection import inspect
class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class User(db.Model, Serializer):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    phone = db.Column(db.String(20))
    img = db.Column(db.String(128))

    def serialize(self):
        d = Serializer.serialize(self)
        del d['password']
        return d

class Shop(db.Model, Serializer):
    __tablename__ = 'shop'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(128))
    salesVolumes = db.Column(db.Integer, default=0)
    productAmount = db.Column(db.Integer, default=0)
    img = db.Column(db.String(128))

    def serialize(self):
        d = Serializer.serialize(self)
        return d

class Product(db.Model, Serializer):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sid = db.Column(db.Integer, db.ForeignKey('shop.id'))
    name = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(128))
    salesVolumes = db.Column(db.Integer, default=0)
    shop = db.Column(db.String(32), nullable=False)
    type = db.Column(db.Text)
    img = db.Column(db.String(128))

    def serialize(self):
        d = Serializer.serialize(self)
        return d

class SalesVolumes(db.Model, Serializer):
    __tablename__ = 'salesVolumes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    sid = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    sales = db.Column(db.Text)

    def serialize(self):
        d = Serializer.serialize(self)
        return d

def db_init():
    # 初始化数据库
    print('创建数据库')
    db.drop_all()
    db.create_all()