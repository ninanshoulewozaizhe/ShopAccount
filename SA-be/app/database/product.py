from app.database.models import Product
from app.database import db
from app.database.models import Product
from app.database import db

preview_count = 4

def get_preview_prodcuts_by_sid(sid):
    products = Product.query.filyer_by(sid=sid).slice(0,preview_count).all()
    return products

def get_all_products_by_sid(sid):
    products = Product.query.filyer_by(sid=sid).all()
    return products

def update_product_info(newInfo):
    product = Product.query.filyer_by(id=newInfo.id).first()
    product.name = newInfo.name
    product.description = newInfo.description
    product.status = newInfo.status
    product.type = newInfo.type
    product.cost = newInfo.cost
    product.price = newInfo.price
    db.session.commit()

def update_product_img(pid, img):
    product = Product.query.filter_by(id=pid).first()
    product.img = img
    db.session.commit()

def update_product_sales(pid, salesVolumes):
    product = Product.query.filter_by(id=pid).first()
    product.salesVolumes = salesVolumes
    db.session.commit()

def delete_product_by_pid(pid):
    product = Product.query.filter_by(id=pid).first()
    db.session.delete(product)
    db.session.commit()

def delete_products_by_sid(sid):
    products = Product.query.filter_by(sid=sid).all()
    db.session.delete(products)
    db.session.commit()
