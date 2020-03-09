import json
import os
import cv2
import time
import random
import numpy as np
from werkzeug.utils import secure_filename
from app.log import logger

def form2Dict(form, key_dict):
    result = {}
    for key in key_dict.keys():
        result[key] = form.get(key, key_dict[key])
    return result

def getSalesCountfromSalesStr(sales):
    result = 0
    sales = json.loads(sales)
    for value in sales.values():
        result += value
    return result

def create_UPicId():
        timestamp = int(time.time())
        randomNum = random.randint(0, 100)
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        UPicId = str(timestamp) + str(randomNum)
        return UPicId

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img

def imgSave(imgfile, imgPrefix):
    # 当前文件所在路径
    basepath = os.path.dirname(__file__)
    UPLOAD_TMEP_PATH = r'static\images\temp'
    upload_temp_path = os.path.join(basepath, UPLOAD_TMEP_PATH, secure_filename(imgfile.filename))  
    imgfile.save(upload_temp_path)
    logger.info(f'images save succeed, path: {upload_temp_path}')

    # 使用Opencv转换一下图片格式和名称
    img = cv_imread(upload_temp_path)
    if img is None:
        logger.info(f'转换失败，读取不到图片')

    upid = create_UPicId()
    imgName = f'{imgPrefix}-{upid}.png'
    FINAL_PATH = r'static\images'
    cv2.imencode('.png', img)[1].tofile(os.path.join(basepath, FINAL_PATH, imgName))

    logger.info(f'转后图片名称: {imgName}')

    return imgName
