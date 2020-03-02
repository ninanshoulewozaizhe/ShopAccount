from flask import Flask

# 支持跨域
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = '*'
    return resp

app = Flask(__name__)
app.after_request(after_request)

