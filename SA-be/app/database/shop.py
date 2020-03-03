from app.database.models import Shop
from app.database import db


def create_shop(shop):
    with db.auto_commit_db():
        new_shop = shop(name=shop['name'], description=shop['description'], img=shop['img'], uid=shop['uid'])
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
    shop = Shop.query.filter_by(id=newInfo['id']).first()
    if shop is not None:
        shop.name = newInfo['name']
        shop.description = newInfo['description']
        db.session.commit()
        return True
    else:
        return False

def update_shop_img(sid, img):
    shop = Shop.query.filter_by(id=sid).first()
    if shop is not None:
        shop.img = img
        db.session.commit()
        return True
    else:
        return False

def delete_shop(sid):
    shop = Shop.query.filter_by(id=sid).first()
    if shop is not None:
        db.session.delete(shop)
        db.session.commit()
        return True
    else:
        return False

def increase_shop_sales(sid, salesVolumes):
    shop = Shop.query.filter_by(id=sid).first()
    if shop is not None:
        shop.salesVolumes += salesVolumes
        db.session.commit()
        return True
    else:
        return False

def increase_shop_product_amount(sid, amount):
    shop = Shop.query.filter_by(id=sid).first()
    if shop is not None:
        shop.productAmount += amount
        db.session.commit()
        return True
    else:
        return False
