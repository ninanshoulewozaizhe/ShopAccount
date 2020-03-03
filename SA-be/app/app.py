from flask import Flask
import os

# 支持跨域
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

app = Flask(__name__)
# app 配置
app.after_request(after_request)
app.config['SECRET_KEY'] = os.urandom(24)

