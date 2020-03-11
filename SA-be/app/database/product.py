from app.database.models import Product
from app.database import db
import json
import ast

def create_product(product):
    with db.auto_commit_db():
        new_product = Product(name=product['name'], status=product['status'], description=product['description'],
            shop=product['shop'], sid=product['sid'], type=product['type'], img=product['img'])
        db.session.add(new_product)
        db.session.flush()
        pid = new_product.id
    return pid

def get_preview_prodcuts_by_sid(sid, preview_count):
    products = Product.query.filter_by(sid=sid).slice(0,preview_count).all()
    return products

def get_product_detail_by_pid(pid):
    product = Product.query.filter_by(id=pid).first()
    return product


def get_all_products_by_sid(sid):
    products = Product.query.filter_by(sid=sid).all()
    return products

def update_product_info(newInfo):
    product = Product.query.filter_by(id=newInfo['id']).first()
    if product is not None:
        product.name = newInfo['name']
        product.img = newInfo['img']
        product.description = newInfo['description']
        product.status = newInfo['status']
        product.type = newInfo['type']
        db.session.commit()
        return True
    else:
        return False

def update_product_img(pid, img):
    product = Product.query.filter_by(id=pid).first()
    if product is not None:
        product.img = img
        db.session.commit()
        return True
    else:
        return False

def update_product_sales(pid, salesVolumes):
    product = Product.query.filter_by(id=pid).first()
    if product is not None:
        product.salesVolumes = salesVolumes
        db.session.commit()
        return True
    else:
        return False

def update_product_inventory(pid, increase, sales):
    product = Product.query.filter_by(id=pid).first()
    if product is not None:
        originTypeInventory = json.loads(product.type)
        sales = json.loads(sales)
        for key in sales.keys():
            if key in originTypeInventory.keys():
                if increase:
                    originTypeInventory[key] += int(sales[key])
                else:
                    originTypeInventory[key] -= int(sales[key])
        product.type = json.dumps(originTypeInventory)
        db.session.commit()
        return True
    else:
        return False

def increase_product_sales(pid, ISalesVolumes):
    product = Product.query.filter_by(id=pid).first()
    if product is not None:
        product.salesVolumes += ISalesVolumes
        db.session.commit()
        return True
    else:
        return False

def delete_product_by_pid(pid):
    product = Product.query.filter_by(id=pid).first()
    if product is not None:
        sid = product.sid
        db.session.delete(product)
        db.session.commit()
        return True, sid
    else:
        return False, -1

def delete_products_by_sid(sid):
    Product.query.filter_by(sid=sid).delete()
    db.session.commit()
    return True

