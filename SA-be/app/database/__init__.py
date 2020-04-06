from app.database.sqlaichemy import SQLAlchemy
from app import app
import app.database.config as config
db = SQLAlchemy()
from app.database.models import db_init


def app_db_init():
    # 关联db的config.py文件
    app.config.from_object(config)
    # db关联app
    db.init_app(app)
    db.app = app


    # 数据库初始化
    # db_init()
