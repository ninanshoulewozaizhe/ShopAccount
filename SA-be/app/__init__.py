from flask import Flask, render_template, request, jsonify, session, escape
from app.app import app
from app.database.models import db_init, User, Product, Shop, SalesVolumes
from app.database.user import create_user, username_exist, \
    user_verification, update_user_info, get_uid_by_username
from app.database.shop import create_shop, get_user_all_shops, get_shop_detail, \
    update_shop_info, update_shop_img, delete_shop, increase_shop_sales, \
    increase_shop_product_amount
from app.database.product import create_product, get_preview_prodcuts_by_sid, \
    get_all_products_by_sid, update_product_info, update_product_img, \
    update_product_sales, increase_product_sales, delete_product_by_pid, \
    delete_products_by_sid, get_product_detail_by_pid
from app.utils import form2Dict
from app.log import logger
import json

# #数据库初始化
# db_init()

@app.route('/')
def hello():
    return 'Welcome to My test!'

@app.route('/testimg')
def testimg():
    return render_template('index.html')

# user登录controller
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            exist = username_exist(session.get('username'))
            if exist[0]:
                logger.info(f'user login, username:{session.get("username")}')
                return jsonify(status=True, message=f'user: {session.get("username")} login', data=exist[1].serialize())
            else:
                return jsonify(status=False, message=f'user invaild', data='')
        else:
            return jsonify(status=False, message='no session', data='')
    else:
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        print(username, password)
        if username == '' or password == '':
            print('error')
            return jsonify(status=False, message='invaid data', data='')
        else:
            print('useful')
            userInfo = {'username': username, 'password': password}
            available, user = user_verification(userInfo)
            if available:
                session['username'] = userInfo['username']
                session.permanent = True
                return jsonify(status=True, message='ok', data=user.serialize())
            else:
                return jsonify(status=False, message='user invaild', data='')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        username = request.args.get('username')
        exist = username_exist(username)
        if exist[0]:
            logger.warning(f'register failed, username:{username} has existed')
            return jsonify(status=False, message="username has existed", data='')
        else:
            logger.info('username available')
            return jsonify(status=True, message="username available", data='')
    else:
        userInfo = form2Dict(request.form, {'username': '', 'password': '', 'phone': ''})
        status, uid = create_user(userInfo)
        if status:
            return jsonify(status=True, message="succeed", data={'uid': uid})
        else:
            return jsonify(status=False, message="failed", data='')


@app.route('/logout', methods=['PUT'])
def logout():
    logger.info(f'user: {session.get("username")} logout')
    session.pop('username', None)
    return jsonify(status=True, message="user logout", data='')

# 商品controller
@app.router('/product', methods=['POST'])
def createProduct():
    productInfo = form2Dict(request.form, {'name': '', 'status':'on-sale', 'description': '', \
        'img': '', 'sid': '-1', 'shop': '', 'type':'', 'salesVolumes': 0, 'cost': 0, 'price': 0})
    status = create_product(productInfo)
    return jsonify(status=True, message='succeed', data={'pid': status[1]})

@app.route('/products', methods=['GET'])
def getAllproducts():
    username = session.get('username')
    uid = get_uid_by_username(username)
    shops = get_user_all_shops(uid)
    allProducts = []
    for shop in shops:
        products = get_all_products_by_sid(shop.id)
        allProducts.extend(Product.serialize_list(products))
    return jsonify(status=True, message='all products', data=allProducts)

@app.route('/product/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def getProductDetai(pid):
    if request.method == 'GET':
        product = get_product_detail_by_pid(pid).serialize()
        return jsonify(status=True, message='succeed', data=product)
    # update product info
    elif request.method == 'PUT':
        productInfo = form2Dict(request.form, {'id':'-1', 'name': '', 'status':'on-sale', \
            'description': '', 'type':'', 'cost': 0, 'price': 0})
        status = update_product_info(productInfo)
        if status:
            return jsonify(status=True, message='succeed', data='')
        else:
            return jsonify(status=False, message='failed', data='')
    else:
        
@app.route('/productImg/<int:pid>', methods=['PUT'])
def updateProductImg(pid):
    pass

# 店铺controller
@app.route('/shops', methods=['GET'])
def getAllShops():
    username = session.get('username')
    uid = get_uid_by_username(username)
    shops = get_user_all_shops(uid)
    shops = Shop.serialize_list(shops)
    return jsonify(status=True, message='all shops', data=shops)

@app.route('/createShop', methods=['POST'])
def createShop():
    username = session.get('username')
    uid = get_uid_by_username(username)
    shopInfo = form2Dict(request.json, {'name': '', 'description': '', 'img': '', 'uid': uid})
    status = create_shop(shopInfo)
    return jsonify(status=True, message='succeed', data={'sid': status[1]})

@app.route('/shop/<int:sid>', method=['GET'])
def getShopDetail(sid):
    shop = get_shop_detail(sid)
    return jsonify(status=True, message='succeed', data=shop.serialize())

@app.route('/shopPreProducts/<int:sid>', method=['GET'])
def getShopPreProducts(sid):
    preview_count = request.args.get('preview_count', 4)
    products = get_preview_prodcuts_by_sid(sid, preview_count)
    products = Product.serialize_list(products)
    return jsonify(status=True, message='succeed', data=products)
    


# # 处理所有错误
# @app.errorhandler(Exception)
# def all_exception_handler(e):
#     return 'Error', 500
