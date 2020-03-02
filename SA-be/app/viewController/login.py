from flask import url_for, request, jsonify
from app.app import app
from app.database.user import create_user, username_exist, \
    user_verification, update_user_info
import json

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if username == '' or password == '':
        return jsonify(message='error', data='invaid data')
    else:
        userInfo = json.dumps({'username': username, 'password': password})
        available, user = user_verification(userInfo)
        if available:
            return jsonify(message='ok', data=user)
        else:
            return jsonify(message='ok', data='')
