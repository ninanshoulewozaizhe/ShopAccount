from app.database.models import SalesVolumes
from app.database import db

def create_new_record(record):
    with db.auto_commit_db():
        new_sales = SalesVolumes(pid=record.pid, date=record.date, sales=record.sales)
        db.session.add(new_sales)
        db.session.flush()
        uid = new_sales.id
    return uid

def get_sales_one_day(pid, date):
    record = SalesVolumes.query.filter_by(pid=pid, date=date).first()
    return record.sales

def get_records_by_period(pid, start, end):
    records = SalesVolumes.query.filter_by(pid=pid) \
        .filter((SalesVolumes.date <= end) & (SalesVolumes.date >= start))
    return records

def update_record_sales(pid, date, sales):
    record = SalesVolumes.query.filter_by(pid=pid, date=date).first()
    record.sales = sales
    db.session.commit()

def delete_record(pid, date):
    record = SalesVolumes.query.filter_by(pid=pid, date=date).first()
    db.session.delete(record)
    db.session.commit()

def delete_records_by_date(date):
    records = SalesVolumes.query.filter_by(date=date).all()
    db.session.delete(records)
    db.session.commit()