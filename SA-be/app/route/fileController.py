from flask import Flask, Blueprint, request, jsonify, session, make_response
from app.route.requestHandler import user_session_check
from app.log import logger
from app import app
import os

file_controller = Blueprint('file_controller', __name__)
file_controller.before_request(user_session_check)

@file_controller.route('/getImg', methods=['GET'])
def getImgFile():
    fileName = request.args.get('f', None)
    logger.info(f'try to get: {fileName}')
    if fileName is None:
        return jsonify(status=False, message='no filename', data='')
    else:
        filePath = os.path.join(app.config['BASE_PATH'], app.config['UPLOAD_FILE_FOLDER'], fileName)
        file = open(filePath, "rb").read()
        response = make_response(file)
        response.headers['Content-Type'] = 'image/png'
        return response
