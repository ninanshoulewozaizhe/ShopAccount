from flask import Blueprint, request, jsonify, session
from app.database.user import create_user, username_exist, phone_exist, \
    user_verification, update_user_info, get_uid_by_username
from app.utils import form2Dict, getSalesCountfromSalesStr, imgSave
from app.log import logger
from datetime import date
import json

user_controller = Blueprint('user_controller', __name__)

# user登录controller
@user_controller.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            exist = username_exist(session.get('username'))
            if exist[0]:
                logger.info(f'user login, username:{session.get("username")}')
                return jsonify(status=True, message=f'user: {session.get("username")} login', data=exist[1].serialize())
            else:
                return jsonify(status=False, message=f'user invaild', data='')
        else:
            return jsonify(status=False, message='no session', data='')
    else:
        username = request.json.get('username', '')
        password = request.json.get('password', '')
        print(username, password)
        if username == '' or password == '':
            print('error')
            return jsonify(status=False, message='invaid data', data='')
        else:
            print('useful')
            userInfo = {'username': username, 'password': password}
            available, user = user_verification(userInfo)
            if available:
                session['username'] = userInfo['username']
                session.permanent = True
                return jsonify(status=True, message='ok', data=user.serialize())
            else:
                return jsonify(status=False, message='user invaild', data='')

@user_controller.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        username = request.args.get('username')
        exist = username_exist(username)
        if exist[0]:
            logger.warning(f'register failed, username:{username} has existed')
            return jsonify(status=False, message="username has existed", data='')
        else:
            logger.info('username available')
            return jsonify(status=True, message="username available", data='')
    else:
        userInfo = form2Dict(request.json, {'username': '', 'password': '', 'phone': ''})
        status, uid = create_user(userInfo)
        if status:
            return jsonify(status=True, message="succeed", data={'uid': uid})
        else:
            return jsonify(status=False, message="failed", data='')


@user_controller.route('/checkPhone', methods=['GET'])
def checkPhone():
    phone = request.args.get('phone')
    exist = phone_exist(phone)
    if exist[0]:
        logger.warning(f'register failed, phone:{phone} has existed')
        return jsonify(status=False, message="phone has existed", data='')
    else:
        logger.info('phone available')
        return jsonify(status=True, message="phone available", data='')

@user_controller.route('/userImg', methods=['POST', 'PUT'])
def uploadUserImg():
    img = request.files['file']
    if img is None:
        return jsonify(status=False, message="img not existed", data='')
    username = session.get('username')
    imgName = f'{username}.png'
    imgSave(img, imgName)
    return jsonify(status=True, message="img upload succeed", data=imgName)

@user_controller.route('/logout', methods=['PUT'])
def logout():
    logger.info(f'user: {session.get("username")} logout')
    session.pop('username', None)
    return jsonify(status=True, message="user logout", data='')
