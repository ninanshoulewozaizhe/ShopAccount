from flask import request, jsonify, session
from app.log import logger

def user_session_check():
    if 'username' not in session:
        logger.warning('user not login')
        return jsonify(status=False, message='user not login', data='')
    else:
        return None