from flask import Blueprint, request, jsonify, session
from app.database.models import User, Product, Shop, SalesVolumes
from app.database.user import get_uid_by_username
from app.database.product import delete_products_by_sid, get_preview_prodcuts_by_sid
from app.database.shop import create_shop, get_user_all_shops, get_shop_detail, \
    update_shop_info, update_shop_img, delete_shop, increase_shop_sales, \
    increase_shop_product_amount
from app.database.salesVolumes import delete_records_by_sid
from app.utils import form2Dict, getSalesCountfromSalesStr
from app.log import logger
from datetime import date
import json
from app.route.requestHandler import user_session_check

shop_controller = Blueprint('shop_controller', __name__)
shop_controller.before_request(user_session_check)

@shop_controller.route('/createShop', methods=['POST'])
def createShop():
    username = session.get('username')
    uid = get_uid_by_username(username)
    shopInfo = form2Dict(request.form, {'name': '', 'description': '', 'img': '', 'uid': uid})
    logger.info(f'user: {username} try to create shop:{shopInfo}')
    sid = create_shop(shopInfo)
    logger.info(f'shop-id: {sid} created')
    return jsonify(status=True, message='succeed', data={'sid': sid})


@shop_controller.route('/shops', methods=['GET'])
def getAllShops():
    username = session.get('username')
    uid = get_uid_by_username(username)
    logger.info(f'user: {username} uid: {uid}, try to get all shops')
    shops = get_user_all_shops(uid)
    shops = Shop.serialize_list(shops)
    return jsonify(status=True, message='all shops', data=shops)
    

@shop_controller.route('/shop/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
def shopHandler(sid):
    # get shop info
    if request.method == 'GET':
        shop = get_shop_detail(sid)
        logger.info(f'try to get shop: id: {sid} info')
        return jsonify(status=True, message='succeed', data=shop.serialize())
    # update shop info
    elif request.method == 'PUT':
        shopInfo = form2Dict(request.json, {'id': sid, 'name': '', 'description': ''})
        logger.info(f'try to update shop: id: {sid} info: {shopInfo}')
        status = update_shop_info(shopInfo)
        if status:
            logger.info(f'succeed to update shop: id: {sid} info')
            return jsonify(status=True, message='succeed', data='')
        else:
            logger.info(f'fail to update shop: id: {sid} info')
            return jsonify(status=False, message='failed', data='')
    # delete shop
    else:
        # 首先删除销量数据和店铺商品
        logger.info(f'try to delete shop: id: {sid} info')
        delete_records_by_sid(sid)
        delete_products_by_sid(sid)
        status = delete_shop(sid)
        if status:
            return jsonify(status=True, message='succeed', data='')
        else:
            return jsonify(status=False, message='failed', data='')

@shop_controller.route('/shopPreProducts/<int:sid>', methods=['GET'])
def getShopPreProducts(sid):
    preview_count = request.args.get('preview_count', 4)
    products = get_preview_prodcuts_by_sid(sid, preview_count)
    products = Product.serialize_list(products)
    return jsonify(status=True, message='succeed', data=products)
    
@shop_controller.route('/shopImg/<int:sid>', methods=['PUT'])
def updateShopImg(sid):
    pass
