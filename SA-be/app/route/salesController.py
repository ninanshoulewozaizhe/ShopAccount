from flask import Blueprint, request, jsonify, session
from app.database.models import User, Product, Shop, SalesVolumes
from app.database.user import get_uid_by_username
from app.database.product import increase_product_sales
from app.database.shop import increase_shop_sales
from app.database.salesVolumes import create_new_record, get_sales_one_day, \
    get_records_by_period, update_record_sales, delete_records_by_date, \
    delete_record    
from app.utils import form2Dict, getSalesCountfromSalesStr
from app.log import logger
from datetime import date
import json

sales_controller = Blueprint('sales_controller', __name__)

# 销量记录controller
@sales_controller.route('/createSalesRecord', methods=['POST'])
def createSalesRecord():
    recordInfo = form2Dict(request.form, {'pid': '', 'sid': '', 'date': date.today().isoformat(), 'sales': ''})
    rid = create_new_record(recordInfo)
    salesCount = getSalesCountfromSalesStr(request.form.get('sales', {}))
    # 更新商品、店铺销量
    increase_product_sales(request.form.get('pid', -1), salesCount)
    increase_shop_sales(request.form.get('sid', '-1'), salesCount)
    return jsonify(status=True, message='succeed', data={'rid': rid})

@sales_controller.route('/salesRecord/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def salesRecordHandler(pid):
    # get record info
    if request.method == 'GET':
        rdate = request.args.get('date', date.today().isoformat())
        rdate = date.fromisoformat(rdate)
        sales = get_sales_one_day(pid, rdate)
        return jsonify(status=True, message='succeed', date=sales)
    # update record info
    elif request.method == 'PUT':
        recordDate = request.json.get('date', date.today().isoformat())
        recordDate = date.fromisoformat(recordDate)
        sales = request.json.get('sales', '')
        status = update_record_sales(pid, recordDate, sales)
        if status:
            return jsonify(status=True, message='succeed', data='')
        else:
            return jsonify(status=False, message='failed', data='')
    # delete record
    else:
        recordDate = request.json.get('date', date.today().isoformat())
        recordDate = date.fromisoformat(recordDate)
        status = delete_record(pid, recordDate)
        if status:
            return jsonify(status=True, message='succeed', data='')
        else:
            return jsonify(status=False, message='failed', data='')

@sales_controller.route('/salesRecordsPeriod/<int:pid>', methods=['GET'])
def getSalesRecordPeriod(pid):
    dateFrom = request.args.get('from', date.today().isoformat())
    dateTo = request.args.get('to', date.today().isoformat())
    records = get_records_by_period(pid, dateFrom, dateTo)
    records = SalesVolumes.serialize_list(records)
    return jsonify(status=True, message='succeed', data='')
