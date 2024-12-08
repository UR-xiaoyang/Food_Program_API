from 控制台输出 import 输出日志
from 数据库.联系数据库 import 连接数据库, 关闭数据库

def 记录日志(操作, IP, 操作人):
    try:
        数据库连接请求, cursor = 连接数据库()
        cursor.execute(f"INSERT INTO log (operation_time, operation, ip_address, user) VALUES (NOW(), '{操作}', '{IP}', '{操作人}')")
        数据库连接请求.commit()
        输出日志(操作, IP, 操作人)
    finally:
        关闭数据库(数据库连接请求,cursor)

# 测试
def debug():
    记录日志("记录日志测试", "127.0.0.1", "DEBUG")

# debug()


