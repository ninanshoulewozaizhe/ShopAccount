from flask import Blueprint, request, jsonify, session
from app.database.models import User, Product, Shop, SalesVolumes
from app.database.user import get_uid_by_username
from app.database.product import increase_product_sales, update_product_inventory
from app.database.shop import increase_shop_sales, get_user_all_shops
from app.database.salesVolumes import create_new_record, get_record_one_day, \
    get_records_by_period, update_record_sales, delete_records_by_date, \
    delete_record, get_shop_records_one_day, get_shop_records_by_period    
from app.utils import form2Dict, getSalesCountfromSalesStr
from app.log import logger
from datetime import date
import json
import ast
from app.route.requestHandler import user_session_check

sales_controller = Blueprint('sales_controller', __name__)
sales_controller.before_request(user_session_check)

# 销量记录controller
@sales_controller.route('/createSalesRecord', methods=['POST'])
def createSalesRecord():
    recordInfo = form2Dict(request.json, {'pid': '', 'sid': '', 'pname': '', 'date': date.today().isoformat(), 'sales': ''})
    recordInfo['date'] = date.fromisoformat(recordInfo['date'])
    recordInfo['sales'] = json.dumps(ast.literal_eval(recordInfo['sales']))
    rid = create_new_record(recordInfo)
    salesCount = getSalesCountfromSalesStr(recordInfo['sales'])
    # 更新库存
    update_product_inventory(recordInfo['pid'], False, recordInfo['sales'])
    # 更新商品、店铺销量
    increase_product_sales(recordInfo['pid'], salesCount)
    increase_shop_sales(recordInfo['sid'], salesCount)
    return jsonify(status=True, message='succeed', data={'rid': rid})

@sales_controller.route('/shopSalesRecords/<int:sid>', methods=['GET'])
def getShopSalesOneDay(sid):
    rdate = request.args.get('date', date.today().isoformat())
    rdate = date.fromisoformat(rdate)
    records = get_shop_records_one_day(sid, rdate)
    records = SalesVolumes.serialize_list(records)
    return jsonify(status=True, message='succeed', data=records)

@sales_controller.route('/salesRecord/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def salesRecordHandler(pid):
    # get record info
    if request.method == 'GET':
        rdate = request.args.get('date', date.today().isoformat())
        rdate = date.fromisoformat(rdate)
        record = get_record_one_day(pid, rdate)
        if record is None:
            return jsonify(status=False, message='failed', data='')
        return jsonify(status=True, message='succeed', data=record.serialize())
    # update record info
    elif request.method == 'PUT':
        recordDate = request.json.get('date', date.today().isoformat())
        recordDate = date.fromisoformat(recordDate)
        newSales = json.dumps(ast.literal_eval(request.json.get('sales', '')))
        # 更新记录表
        originRecord = get_record_one_day(pid, recordDate)
        if originRecord is not None:
            originSalesCount = getSalesCountfromSalesStr(originRecord.sales)
            newSalesCount = getSalesCountfromSalesStr(newSales)
            # 更新各销量
            update_record_sales(pid, recordDate, newSales)
            increase_shop_sales(originRecord.sid, newSalesCount - originSalesCount)
            increase_product_sales(pid, newSalesCount - originSalesCount)
            # 更新商品库存
            update_product_inventory(pid, True, originRecord.sales)
            update_product_inventory(pid, False, newSales)
            return jsonify(status=True, message='succeed', data='')
        else:
            recordInfo = form2Dict(request.json, {'pid': '', 'sid': '', 'pname': '', 'date': date.today().isoformat(), 'sales': ''})
            recordInfo['date'] = date.fromisoformat(recordInfo['date'])
            recordInfo['sales'] = json.dumps(ast.literal_eval(recordInfo['sales']))
            rid = create_new_record(recordInfo)
            salesCount = getSalesCountfromSalesStr(recordInfo['sales'])
            # 更新库存
            update_product_inventory(recordInfo['pid'], False, recordInfo['sales'])
            # 更新商品、店铺销量
            increase_product_sales(recordInfo['pid'], salesCount)
            increase_shop_sales(recordInfo['sid'], salesCount)
            return jsonify(status=True, message='create new record', data={'rid': rid})
    # delete record
    else:
        recordDate = request.json.get('date', date.today().isoformat())
        recordDate = date.fromisoformat(recordDate)
        originRecord = get_record_one_day(pid, recordDate)
        if originRecord  is not None:
            originSalesCount = getSalesCountfromSalesStr(originRecord['sales'])
            # 减少商品销量
            increase_shop_sales(originRecord['sid'], -originSalesCount)
            increase_product_sales(pid, -originSalesCount)
            # 恢复库存
            update_product_inventory(pid, True, originRecord['sales'])
            delete_record(pid, recordDate)
            return jsonify(status=True, message='succeed', data='')
        else:
            return jsonify(status=False, message='failed', data='')

@sales_controller.route('/salesRecordsPeriod/<int:pid>', methods=['GET'])
def getSalesRecordPeriod(pid):
    dateFrom = request.args.get('from', date.today().isoformat())
    dateTo = request.args.get('to', date.today().isoformat())
    logger.info(f'get product {pid} records from:{dateFrom}, to :{dateTo}')
    records = get_records_by_period(pid, date.fromisoformat(dateFrom), date.fromisoformat(dateTo))
    records = SalesVolumes.serialize_list(records)
    return jsonify(status=True, message='succeed', data=records)

@sales_controller.route('/shopSalesPeriod/<int:sid>', methods=['GET'])
def getShopSalesRecordPeriod(sid):
    dateFrom = request.args.get('from', date.today().isoformat())
    dateTo = request.args.get('to', date.today().isoformat())
    logger.info(f'get product {sid} records from:{dateFrom}, to :{dateTo}')
    records = get_shop_records_by_period(sid, date.fromisoformat(dateFrom), date.fromisoformat(dateTo))
    records = SalesVolumes.serialize_list(records)
    return jsonify(status=True, message='succeed', data=records)

@sales_controller.route('/allShopsSalesOneDay', methods=['GET'])
def getAllshopsSalesOneDay():
    rdate = request.args.get('date', date.today().isoformat())
    rdate = date.fromisoformat(rdate)
    username = session.get('username')
    uid = get_uid_by_username(username)
    shops = get_user_all_shops(uid)
    result = {}
    for shop in shops:
        records = get_shop_records_one_day(shop.id, rdate)
        records = SalesVolumes.serialize_list(records)
        result[shop.name] = records
    return jsonify(status=True, message='succeed', data=result)

    
        