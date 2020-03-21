from flask import Blueprint, request, jsonify, session
from app.database.models import User, Product, Shop, SalesVolumes
from app.database.user import get_uid_by_username
from app.database.product import delete_products_by_sid, get_preview_prodcuts_by_sid
from app.database.shop import create_shop, get_user_all_shops, get_shop_detail, \
    update_shop_info, update_shop_img, delete_shop, increase_shop_sales, \
    increase_shop_product_amount
from app.database.salesVolumes import delete_records_by_sid
from app.utils import form2Dict, getSalesCountfromSalesStr, imgSave
from app.log import logger
from datetime import date
import json
import os
from app import app
from app.route.requestHandler import user_session_check

shop_controller = Blueprint('shop_controller', __name__)
shop_controller.before_request(user_session_check)

@shop_controller.route('/createShop', methods=['POST'])
def createShop():
    username = session.get('username')
    uid = get_uid_by_username(username)
    shopInfo = form2Dict(request.json, {'name': '', 'description': '', 'img': '', 'uid': uid})
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
    if shops is None:
        return jsonify(status=False, message='user has no shops', data='')
    else:
        shops = Shop.serialize_list(shops)
        for shop in shops:
            preProducts = get_preview_prodcuts_by_sid(shop['id'], 4)
            preProductImgs = []
            for product in preProducts:
                preProductImgs.append(product.img)
            shop['preProductImgs'] = preProductImgs
        return jsonify(status=True, message='all shops', data=shops)
    

@shop_controller.route('/shop/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
def shopHandler(sid):
    # get shop info
    if request.method == 'GET':
        shop = get_shop_detail(sid)
        logger.info(f'try to get shop: id: {sid} info')
        if shop is None:
            return jsonify(status=False, message='shop not existed', data='')
        else:
            shop = shop.serialize()
            return jsonify(status=True, message='succeed', data=shop)
    # update shop info
    elif request.method == 'PUT':
        shopInfo = form2Dict(request.json, {'id': sid, 'name': '', 'description': '', 'img': ''})
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
    
@shop_controller.route('/shopImg/<int:sid>', methods=['POST'])
def updateShopImg(sid):
    img = request.files['file']
    if img is None:
        return jsonify(status=False, message="img not existed", data='')
    username = session.get('username')
    imgPrefix = username + '-shop'
    imgName = imgSave(img, imgPrefix)
    shop = get_shop_detail(sid)
    originImg = shop.img
    if originImg is not None:
        originImgPath = os.path.join(app.instance_path, r'app\static\images', originImg)
        os.remove(originImgPath)
    update_shop_img(sid, imgName)
    return jsonify(status=True, message="img upload succeed", data=imgName)

@shop_controller.route('/shopImg', methods=['POST'])
def uploadShopImg():
    img = request.files['file']
    if img is None:
        return jsonify(status=False, message="img not existed", data='')
    username = session.get('username')
    imgPrefix = username + '-shop'
    imgName = imgSave(img, imgPrefix)
    return jsonify(status=True, message="img upload succeed", data=imgName)
