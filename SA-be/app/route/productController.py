from flask import Blueprint, request, jsonify, session
from app.database.models import User, Product, Shop, SalesVolumes
from app.database.user import get_uid_by_username
from app.database.product import create_product, get_preview_prodcuts_by_sid, \
    get_all_products_by_sid, update_product_info, update_product_img, \
    update_product_sales, increase_product_sales, delete_product_by_pid, \
    delete_products_by_sid, get_product_detail_by_pid
from app.database.shop import increase_shop_product_amount, get_user_all_shops
from app.database.salesVolumes import delete_records_by_pid
from app.utils import form2Dict, getSalesCountfromSalesStr
from app.log import logger
from datetime import date
import json
import ast
from app.route.requestHandler import user_session_check

product_controller = Blueprint('product_controller', __name__)
product_controller.before_request(user_session_check)

# 商品controller
@product_controller.route('/product', methods=['POST'])
def createProduct():
    productInfo = form2Dict(request.json, {'name': '', 'status':'on-sale', 'description': '', \
        'img': '', 'sid': '-1', 'shop': '', 'type':'', 'salesVolumes': 0})
    productInfo['type'] = json.dumps(ast.literal_eval(productInfo['type']))
    pid = create_product(productInfo)
    increase_shop_product_amount(productInfo['sid'], 1)
    return jsonify(status=True, message='succeed', data={'pid': pid})

@product_controller.route('/products', methods=['GET'])
def getAllproducts():
    username = session.get('username')
    uid = get_uid_by_username(username)
    shops = get_user_all_shops(uid)
    allProducts = []
    for shop in shops:
        products = get_all_products_by_sid(shop.id)
        if products is not None:
            allProducts.extend(Product.serialize_list(products))
    return jsonify(status=True, message='all products', data=allProducts)

@product_controller.route('/products/<int:sid>', methods=['GET'])
def getShopProducts(sid):
    products = get_all_products_by_sid(sid)
    if products is not None:
        products = Product.serialize_list(products)
        for product in products:
            product['type'] = json.loads(product["type"])
        return jsonify(status=True, message='products in shop', data=products)
    else:
        return jsonify(status=False, message='shop has no products', data='')


@product_controller.route('/product/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def productHandler(pid):
    # get product info
    if request.method == 'GET':
        product = get_product_detail_by_pid(pid)
        if product is not None:
            product = product.serialize()
            product["type"] = json.loads(product["type"])
            return jsonify(status=True, message='succeed', data=product)
        else:
            return jsonify(status=False, message='product does not exist', data='')
    # update product info
    elif request.method == 'PUT':
        productInfo = form2Dict(request.json, {'id':'-1', 'name': '', 'status':'on-sale', \
            'description': '', 'type':'', 'cost': 0, 'price': 0})
        productInfo['type'] = json.dumps(ast.literal_eval(productInfo['type']))
        status = update_product_info(productInfo)
        if status:
            return jsonify(status=True, message='succeed', data='')
        else:
            return jsonify(status=False, message='failed', data='')
    # delete product
    else:
        delete_records_by_pid(pid)
        status, sid = delete_product_by_pid(pid)
        if status:
            increase_shop_product_amount(sid, -1)
            return jsonify(status=True, message='succeed', data='')
        else:
            return jsonify(status=False, message='failed', data='') 
        
@product_controller.route('/productImg/<int:pid>', methods=['PUT'])
def updateProductImg(pid):
    pass
