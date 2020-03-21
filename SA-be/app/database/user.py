from app.database.models import User
from app.database import db
from app.log import logger
import hashlib

def create_user(userInfo):
    # 检测账号是否已存在
    logger.info(f'create user: {userInfo}')
    exist = username_exist(userInfo['username'])
    if exist[0]:
        logger.warning('create failed, username exist')
        return False, -1
    # 加密密码
    logger.info(f'{exist}')
    hash_pd = hashlib.sha256(userInfo['password'].encode("utf-8")).hexdigest() 
    logger.info(f"origin: {userInfo['password']}, hashl:{hash_pd}")
    new_user = User(username=userInfo['username'], password=hash_pd, phone=userInfo['phone'])
    db.session.add(new_user)
    db.session.flush()
    uid = new_user.id
    logger.info(f'user create succeed, uid: {uid}')
    db.session.commit()
    return True, uid

def username_exist(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        logger.info(f'exist: {user}')
        return True, user
    else:
        return False, None

def phone_exist(phone):
    user = User.query.filter_by(phone=phone).first()
    if user is not None:
        logger.info(f'exist: {user}')
        return True, user
    else:
        return False, None

def user_verification(userInfo):
    exist, user = username_exist(userInfo['username'])
    if not exist:
        return False, None
    else:
        hash_pd = hashlib.sha256(userInfo['password'].encode("utf-8")).hexdigest()
        if user.password == hash_pd:
            return True, user
        else:
            return False, None

def update_user_password(username, password):
    user = User.query.filter_by(username=username).first()
    user.password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    db.session.commit()

def update_user_phone(username, phone):
    user = User.query.filter_by(username=username).first()
    user.phone = phone
    db.session.commit()

def update_user_img(username, img):
    user = User.query.filter_by(username=username).first()
    user.img = img
    db.session.commit()

def get_uid_by_username(username):
   user = User.query.filter_by(username=username).first()
   return user.id

def get_uImg_by_username(username):
   user = User.query.filter_by(username=username).first()
   return user.img

