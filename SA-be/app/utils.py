import json
import os
import cv2
import time
import random
from werkzeug.utils import secure_filename

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

def imgSave(imgfile, imgPrefix):
    # 当前文件所在路径
    basepath = os.path.dirname(__file__)
    UPLOAD_PATH = 'static/images'

    upload_path = os.path.join(basepath, UPLOAD_PATH, secure_filename(imgfile.filename))  
    imgfile.save(upload_path)

    # 使用Opencv转换一下图片格式和名称
    img = cv2.imread(upload_path)
    upid = create_UPicId()
    imgName = f'{imgPrefix}-{upid}.png'
    cv2.imwrite(os.path.join(basepath, UPLOAD_PATH, imgName), img)

    return imgName
