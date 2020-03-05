from app.database.models import SalesVolumes
from app.database import db
from app.log import logger

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
        logger.info(f'delete record (pid:{pid}, date:{date}) succeed')
        return True
    else:
        logger.info(f'delete record (pid:{pid}, date:{date}) failed, record not exists')
        return False

def delete_records_by_date(date):
    SalesVolumes.query.filter_by(date=date).delete()
    db.session.commit()
    logger.info(f'delete records (date:{date}) succeed')
    return True


def delete_records_by_pid(pid):
    SalesVolumes.query.filter_by(pid=pid).delete()
    db.session.commit()
    logger.info(f'delete records (pid:{pid}) succeed')
    return True

def delete_records_by_sid(sid):
    SalesVolumes.query.filter_by(sid=sid).delete()
    db.session.commit()
    logger.info(f'delete records (sid:{sid}) succeed')
    return True