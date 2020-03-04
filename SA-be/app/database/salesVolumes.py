from app.database.models import SalesVolumes
from app.database import db

def create_new_record(record):
    with db.auto_commit_db():
        new_sales = SalesVolumes(pid=record['pid'], sid=record['sid'], date=record['date'], sales=record['sales'])
        db.session.add(new_sales)
        db.session.flush()
        rid = new_sales.id
    return rid

def get_sales_one_day(pid, date):
    record = SalesVolumes.query.filter_by(pid=pid, date=date).first()
    return record.sales

def get_records_by_period(pid, start, end):
    records = SalesVolumes.query.filter_by(pid=pid) \
        .filter((SalesVolumes.date <= end) & (SalesVolumes.date >= start))
    return records

def update_record_sales(pid, date, sales):
    record = SalesVolumes.query.filter_by(pid=pid, date=date).first()
    if record is not None:
        record.sales = sales
        db.session.commit()
        return True
    else:
        return False

def delete_record(pid, date):
    record = SalesVolumes.query.filter_by(pid=pid, date=date).first()
    if record is not None:
        db.session.delete(record)
        db.session.commit()
        return True
    else:
        return False

def delete_records_by_date(date):
    records = SalesVolumes.query.filter_by(date=date).all()
    if records is not None:
        db.session.delete(records)
        db.session.commit()
        return True
    else:
        return False

def delete_records_by_pid(pid):
    records = SalesVolumes.query.filter_by(pid=pid).all()
    if records is not None:
        db.session.delete(records)
        db.session.commit()
        return True
    else:
        return False

def delete_records_by_sid(sid):
    records = SalesVolumes.query.filter_by(sid=sid).all()
    if records is not None:
        db.session.delete(records)
        db.session.commit()
        return True
    else:
        return False