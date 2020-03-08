from flask import Flask
import app.database.config as config
from app.database.models import db_init
from app.database import db
from app.route.productController import product_controller
from app.route.shopController import shop_controller
from app.route.userController import user_controller
from app.route.salesController import sales_controller
import os

UPLOAD_PATH = 'static/images'

# 支持跨域
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

def create_app():

    app = Flask(__name__)
    # app 配置
    app.after_request(after_request)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['UPLOAD_PATH'] = UPLOAD_PATH
    # 蓝图挂载
    app.register_blueprint(product_controller)
    app.register_blueprint(shop_controller)
    app.register_blueprint(user_controller)
    app.register_blueprint(sales_controller)

    # 关联db的config.py文件
    app.config.from_object(config)
    # db关联app
    db.init_app(app)
    db.app = app

    # #数据库初始化
    # db_init()
    return app


