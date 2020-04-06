from flask import Flask, render_template, request, jsonify, session
# from app.database.models import db_init, User, Product, Shop, SalesVolumes
# from app.database.user import create_user, username_exist, \
#     user_verification, update_user_info, get_uid_by_username
# from app.database.shop import create_shop, get_user_all_shops, get_shop_detail, \
#     update_shop_info, update_shop_img, delete_shop, increase_shop_sales, \
#     increase_shop_product_amount
# from app.database.product import create_product, get_preview_prodcuts_by_sid, \
#     get_all_products_by_sid, update_product_info, update_product_img, \
#     update_product_sales, increase_product_sales, delete_product_by_pid, \
#     delete_products_by_sid, get_product_detail_by_pid
# from app.database.salesVolumes import create_new_record, get_sales_one_day, \
#     get_records_by_period, update_record_sales, delete_records_by_date, \
#     delete_records_by_pid, delete_records_by_sid, delete_record    
# from app.utils import form2Dict, getSalesCountfromSalesStr
from app.log import logger
from datetime import date
import json
import os

app = Flask(__name__)
# app 配置
app.config['SECRET_KEY'] = os.urandom(24)
app.config['BASE_PATH'] = os.path.dirname(__file__)
app.config['UPLOAD_FILE_FOLDER'] = r'static\images'
app.config['UPLOAD_TMEP_FILE_FOLDER'] = r'static\images\temp'

from app.route.requestHandler import after_request
from app.database import app_db_init
from app.route import bp_register

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
app.after_request(after_request)
app_db_init()
bp_register()

@app.route('/', methods=['GET'])
def hello():
    return 'Welcome to My test!'

@app.route('/testimg', methods=['GET'])
def testimg():
    return render_template('index.html')

# # user登录controller
# @app.route('/login', methods=['GET','POST'])
# def login():
#     if request.method == 'GET':
#         if 'username' in session:
#             exist = username_exist(session.get('username'))
#             if exist[0]:
#                 logger.info(f'user login, username:{session.get("username")}')
#                 return jsonify(status=True, message=f'user: {session.get("username")} login', data=exist[1].serialize())
#             else:
#                 return jsonify(status=False, message=f'user invaild', data='')
#         else:
#             return jsonify(status=False, message='no session', data='')
#     else:
#         username = request.form.get('username', '')
#         password = request.form.get('password', '')
#         print(username, password)
#         if username == '' or password == '':
#             print('error')
#             return jsonify(status=False, message='invaid data', data='')
#         else:
#             print('useful')
#             userInfo = {'username': username, 'password': password}
#             available, user = user_verification(userInfo)
#             if available:
#                 session['username'] = userInfo['username']
#                 session.permanent = True
#                 return jsonify(status=True, message='ok', data=user.serialize())
#             else:
#                 return jsonify(status=False, message='user invaild', data='')

# @app.route('/register', methods=['POST', 'GET'])
# def register():
#     if request.method == 'GET':
#         username = request.args.get('username')
#         exist = username_exist(username)
#         if exist[0]:
#             logger.warning(f'register failed, username:{username} has existed')
#             return jsonify(status=False, message="username has existed", data='')
#         else:
#             logger.info('username available')
#             return jsonify(status=True, message="username available", data='')
#     else:
#         userInfo = form2Dict(request.form, {'username': '', 'password': '', 'phone': ''})
#         status, uid = create_user(userInfo)
#         if status:
#             return jsonify(status=True, message="succeed", data={'uid': uid})
#         else:
#             return jsonify(status=False, message="failed", data='')

# @app.route('/logout', methods=['PUT'])
# def logout():
#     logger.info(f'user: {session.get("username")} logout')
#     session.pop('username', None)
#     return jsonify(status=True, message="user logout", data='')

# # 商品controller
# @app.route('/product', methods=['POST'])
# def createProduct():
#     productInfo = form2Dict(request.form, {'name': '', 'status':'on-sale', 'description': '', \
#         'img': '', 'sid': '-1', 'shop': '', 'type':'', 'salesVolumes': 0, 'cost': 0, 'price': 0})
#     pid = create_product(productInfo)
#     increase_shop_product_amount(productInfo['sid'], 1)
#     return jsonify(status=True, message='succeed', data={'pid': pid})

# @app.route('/products', methods=['GET'])
# def getAllproducts():
#     username = session.get('username')
#     uid = get_uid_by_username(username)
#     shops = get_user_all_shops(uid)
#     allProducts = []
#     for shop in shops:
#         products = get_all_products_by_sid(shop.id)
#         allProducts.extend(Product.serialize_list(products))
#     return jsonify(status=True, message='all products', data=allProducts)

# @app.route('/products/<int:sid>', methods=['GET'])
# def getShopProducts(sid):
#     products = get_all_products_by_sid(sid)
#     return jsonify(status=True, message='products in shop', data=Product.serialize_list(products))

# @app.route('/product/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
# def productHandler(pid):
#     # get product info
#     if request.method == 'GET':
#         product = get_product_detail_by_pid(pid).serialize()
#         return jsonify(status=True, message='succeed', data=product)
#     # update product info
#     elif request.method == 'PUT':
#         productInfo = form2Dict(request.form, {'id':'-1', 'name': '', 'status':'on-sale', \
#             'description': '', 'type':'', 'cost': 0, 'price': 0})
#         status = update_product_info(productInfo)
#         if status:
#             return jsonify(status=True, message='succeed', data='')
#         else:
#             return jsonify(status=False, message='failed', data='')
#     # delete product
#     else:
#         delete_records_by_pid(pid)
#         status, sid = delete_product_by_pid(pid)
#         increase_shop_product_amount(sid, -1)
#         if status:
#             return jsonify(status=True, message='succeed', data='')
#         else:
#             return jsonify(status=False, message='failed', data='') 
        
# @app.route('/productImg/<int:pid>', methods=['PUT'])
# def updateProductImg(pid):
#     pass

# # 店铺controller
# @app.route('/createShop', methods=['POST'])
# def createShop():
#     username = session.get('username')
#     uid = get_uid_by_username(username)
#     if uid is not None:
#         shopInfo = form2Dict(request.form, {'name': '', 'description': '', 'img': '', 'uid': uid})
#         sid = create_shop(shopInfo)
#         return jsonify(status=True, message='succeed', data={'sid': sid})
#     else:
#         return jsonify(status=False, message='user no login', data='')

# @app.route('/shops', methods=['GET'])
# def getAllShops():
#     username = session.get('username')
#     uid = get_uid_by_username(username)
#     shops = get_user_all_shops(uid)
#     shops = Shop.serialize_list(shops)
#     return jsonify(status=True, message='all shops', data=shops)


# @app.route('/shop/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
# def shopHandler(sid):
#     # get shop info
#     if request.method == 'GET':
#         shop = get_shop_detail(sid)
#         return jsonify(status=True, message='succeed', data=shop.serialize())
#     # update shop info
#     elif request.method == 'PUT':
#         shopInfo = form2Dict(request.json, {'id':'-1', 'name': '', 'description': ''})
#         status = update_shop_info(shopInfo)
#         if status:
#             return jsonify(status=True, message='succeed', data='')
#         else:
#             return jsonify(status=False, message='failed', data='')
#     # delete shop
#     else:
#         # 首先删除销量数据和店铺商品
#         delete_records_by_sid(sid)
#         delete_products_by_sid(sid)
#         status = delete_shop(sid)
#         if status:
#             return jsonify(status=True, message='succeed', data='')
#         else:
#             return jsonify(status=False, message='failed', data='')

# @app.route('/shopPreProducts/<int:sid>', methods=['GET'])
# def getShopPreProducts(sid):
#     preview_count = request.args.get('preview_count', 4)
#     products = get_preview_prodcuts_by_sid(sid, preview_count)
#     products = Product.serialize_list(products)
#     return jsonify(status=True, message='succeed', data=products)
    
# @app.route('/shopImg/<int:sid>', methods=['PUT'])
# def updateShopImg(sid):
#     pass

# # 销量记录controller
# @app.route('/createSalesRecord', methods=['POST'])
# def createSalesRecord():
#     recordInfo = form2Dict(request.form, {'pid': '', 'sid': '', 'date': date.today().isoformat(), 'sales': ''})
#     rid = create_new_record(recordInfo)
#     salesCount = getSalesCountfromSalesStr(request.form.get('sales', {}))
#     # 更新商品、店铺销量
#     increase_product_sales(request.form.get('pid', -1), salesCount)
#     increase_shop_sales(request.form.get('sid', '-1'), salesCount)
#     return jsonify(status=True, message='succeed', data={'rid': rid})

# @app.route('/salesRecord/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
# def salesRecordHandler(pid):
#     # get record info
#     if request.method == 'GET':
#         rdate = request.args.get('date', date.today().isoformat())
#         rdate = date.fromisoformat(rdate)
#         sales = get_sales_one_day(pid, rdate)
#         return jsonify(status=True, message='succeed', date=sales)
#     # update record info
#     elif request.method == 'PUT':
#         recordDate = request.json.get('date', date.today().isoformat())
#         recordDate = date.fromisoformat(recordDate)
#         sales = request.json.get('sales', '')
#         status = update_record_sales(pid, recordDate, sales)
#         if status:
#             return jsonify(status=True, message='succeed', data='')
#         else:
#             return jsonify(status=False, message='failed', data='')
#     # delete record
#     else:
#         recordDate = request.json.get('date', date.today().isoformat())
#         recordDate = date.fromisoformat(recordDate)
#         status = delete_record(pid, recordDate)
#         if status:
#             return jsonify(status=True, message='succeed', data='')
#         else:
#             return jsonify(status=False, message='failed', data='')

# @app.route('/salesRecordsPeriod/<int:pid>', methods=['GET'])
# def getSalesRecordPeriod(pid):
#     dateFrom = request.args.get('from', date.today().isoformat())
#     dateTo = request.args.get('to', date.today().isoformat())
#     records = get_records_by_period(pid, dateFrom, dateTo)
#     records = SalesVolumes.serialize_list(records)
#     return jsonify(status=True, message='succeed', data='')

# # 处理所有错误
# @app.errorhandler(Exception)
# def all_exception_handler(e):
#     return 'Error', 500
