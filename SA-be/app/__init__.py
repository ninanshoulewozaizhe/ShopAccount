from flask import Flask, url_for, render_template
from app.app import get_app_instance

app = get_app_instance()

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