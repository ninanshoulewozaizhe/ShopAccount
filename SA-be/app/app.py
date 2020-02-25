from flask import Flask


# 创建app实例
def get_app_instance():
    app = Flask(__name__)
    return app

