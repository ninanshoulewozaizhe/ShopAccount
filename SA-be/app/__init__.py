from flask import Flask, render_template, request, jsonify
from app.app import app
from app.database.models import db_init
from app.database.user import create_user, username_exist, \
    user_verification, update_user_info
from app.utils import form2Dict
from app.log import logger
import json

# #数据库初始化
# db_init()

@app.route('/')
def hello():
    return 'Welcome to My test!'

@app.route('/testimg')
def testimg():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    print(username, password)
    if username == '' or password == '':
        print('error')
        return jsonify(status=False, message='invaid data', data='')
    else:
        print('useful')
        userInfo = {'username': username, 'password': password}
        available, user = user_verification(userInfo)
        if available:
            return jsonify(status=True, message='ok', data=user)
        else:
            return jsonify(status=False, message='user invaild', data='')


@app.route('/register', methods=['POST'])
def register():
    userInfo = form2Dict(request.form, {'username': '', 'password': '', 'phone': ''})
    status, uid = create_user(userInfo)
    if status:
        return jsonify(status=True, message="succeed", data={'uid': uid})
    else:
        return jsonify(status=False, message="failed", data='')


# # 处理所有错误
# @app.errorhandler(Exception)
# def all_exception_handler(e):
#     return 'Error', 500
