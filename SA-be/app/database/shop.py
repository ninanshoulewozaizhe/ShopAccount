from app.database.models import Shop
from app.database import db


def create_shop(shop):
    with db.auto_commit_db():
        new_shop = shop(name=shop.name, description=shop.description, img=shop.img)
        db.session.add(new_shop)
        db.session.flush()
        sid = new_shop.id
    return True, sid

def get_user_all_shops(uid):
    shops = Shop.query.filter_by(uid=uid).all()
    return shops

def get_shop_detail(sid):
    shop = Shop.query.filter_by(id=sid).first()
    return shop

def update_shop_info(newInfo):
    shop = Shop.query.filter_by(id=newInfo.id).first()
    shop.name = newInfo.name
    shop.description = newInfo.description
    db.session.commit()

def update_shop_img(sid, img):
    shop = Shop.query.filter_by(id=sid).first()
    shop.img = img
    db.session.commit()

def delete_shop(sid):
    shop = Shop.query.filter_by(id=sid).first()
    db.session.delete(shop)
    db.session.commit()

def increase_shop_sales(sid, salesVolumes):
    shop = Shop.query.filter_by(id=sid).first()
    shop.salesVolumes += salesVolumes
    db.session.commit()

def increase_shop_product_amount(sid, amount):
    shop = Shop.query.filter_by(id=sid).first()
    shop.productAmount += amount
    db.session.commit()
