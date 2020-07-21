from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy
from contextlib import contextmanager

# https://blog.csdn.net/weixin_43343144/article/details/87106213
class  SQLAlchemy(BaseSQLAlchemy):
    #利用contextmanager管理器,对try/except语句封装，使用的时候和with结合
    @contextmanager
    def auto_commit_db(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
           # commit失败，须回滚
           self.session.rollback()
           raise e
