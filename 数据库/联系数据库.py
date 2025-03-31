# 用来导入配置联系数据库
# 导入“数据库配置.py”的class Config中的配置

import pymysql

from 数据库.数据库配置 import Config

# 说明：调用"连接数据库()"用于连接数据库，返回 连接, 光标
# 光标是用来执行命令的
def 连接数据库():
    # 创建连接
    数据库连接请求 = pymysql.connect(
        host=Config.HOST,
        port=int(Config.PORT),
        user=Config.USER,
        password=Config.PASSWORD,
        database=Config.NAME,
        charset="utf8mb4"
    )
    cursor = 数据库连接请求.cursor()
    return 数据库连接请求, cursor

def 关闭数据库(数据库连接请求,cursor):
    cursor.close()
    数据库连接请求.close()