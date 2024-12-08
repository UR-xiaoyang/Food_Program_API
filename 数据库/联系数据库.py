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
        port=Config.PORT,
        user=Config.USER,
        password=Config.PASSWORD,
        database=Config.NAME,
        charset="utf8mb4"
    )
    cursor = 数据库连接请求.cursor()
    # 检测连接状态
    # if 数据库连接请求.open:
    #     print("数据库连接成功")
    # else:
    #     print("数据库连接失败,请检查配置")
    return 数据库连接请求, cursor

def 关闭数据库(数据库连接请求,cursor):
    cursor.close()
    数据库连接请求.close()
    #print("数据库已经关闭")

def debug():
    数据库连接请求,cursor = 连接数据库()
    try:
        # 向log表中插入数据，operation_time为当前时间，operation为“数据库连接测试”，ip_address为127.0.0.1
        cursor.execute("INSERT INTO log (operation_time, operation, ip_address, user) VALUES (NOW(), '数据库连接测试', '127.0.0.1', 'DEBUG')")
        # 提交事务
        数据库连接请求.commit()
        print("数据库连接测试成功")
    finally:
        关闭数据库(数据库连接请求,cursor)

# debug()




