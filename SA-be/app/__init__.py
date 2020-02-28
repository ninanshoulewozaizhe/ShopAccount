from flask import Flask, url_for, render_template
from app.app import app
from app.database.models import db_init

# 数据库初始化
# db_init()

@app.route('/')
def hello():
    return 'Welcome to My test!'


@app.route('/testimg')
def testimg():
    return render_template('index.html')
# 处理所有错误
@app.errorhandler(Exception)
def all_exception_handler(e):
    return 'Error', 500