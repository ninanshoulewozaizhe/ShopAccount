from flask import request, jsonify, session
from app.log import logger
import os

def user_session_check():
    if 'username' not in session:
        logger.warning('user not login')
        return jsonify(status=False, message='user not login', data='')
    else:
        return None

# 支持跨域
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

