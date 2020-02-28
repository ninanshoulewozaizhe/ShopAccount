from flask_sqlalchemy import SQLAlchemy
from app.app import app
import app.database.config as config

# 关联db的config.py文件
app.config.from_object(config)  
# 建立和数据库的关系映射
db = SQLAlchemy(app)