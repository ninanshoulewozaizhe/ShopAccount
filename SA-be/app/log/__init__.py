import logging
import logging.config
from os import path

# 添加配置文件 注意文件路径问题
log_conf_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_conf_file_path)

# 创建logger
logger = logging.getLogger('SALogger')