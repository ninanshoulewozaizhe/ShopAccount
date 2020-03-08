import json
import os
import cv2
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

def imgSave(imgfile, imgName):
    # 当前文件所在路径
    basepath = os.path.dirname(__file__)  
 
    upload_path = os.path.join(basepath, app.config['UPLOAD_PATH'], secure_filename(imgfile.filename))  
    imgfile.save(upload_path)

    # 使用Opencv转换一下图片格式和名称
    img = cv2.imread(upload_path)
    cv2.imwrite(os.path.join(basepath, app.config['UPLOAD_PATH'], imgName), img)
