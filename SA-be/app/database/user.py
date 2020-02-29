from app.database.models import User
from app.database import db
import hashlib

def create_user(userInfo):
    # 检测账号是否已存在
    exist = username_exist(userInfo.username)
    if exist:
        return False, -1
    # 加密密码
    hash_pd = hashlib.sha256(userInfo.password).hexdigest() 
    new_user = User(username=userInfo.username, password=hash_pd, email=userInfo.email)
    db.session.add(new_user)
    db.session.flush()
    uid = new_user.id
    db.session.commit()
    return True, uid

def username_exist(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return True, user
    else:
        return False, None

def user_verification(userInfo):
    exist, user = username_exist(userInfo.username)
    if not exist:
        return False
    else:
        hash_pd = hashlib.sha256(userInfo.password).hexdigest()
        if user.password == hash_pd:
            return True
        else:
            return False

def update_user_info(newInfo):
   user = db.query(User).filter_by(username=newInfo.username).first()
   user.password = hashlib.sha256(newInfo.password).hexdigest()
   user.email = newInfo.email
   db.session.commit()
