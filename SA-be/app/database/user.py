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
    logger.info(f'exist: {user}')
    if user is not None:
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

def update_user_info(newInfo):
    user = User.query.filter_by(username=newInfo['username']).first()
    user.password = hashlib.sha256(newInfo['password'].encode("utf-8")).hexdigest()
    user.phone = newInfo['phone']
    db.session.commit()

def get_uid_by_username(username):
   user = User.query.filter_by(username=username).first()
   return user.id

