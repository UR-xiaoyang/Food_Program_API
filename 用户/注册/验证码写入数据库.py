from 数据库.联系数据库 import 连接数据库, 关闭数据库
from datetime import datetime

def 验证码写入(email, 验证码, IP):
    连接, 光标 = 连接数据库()

    当前时间 = datetime.now()

    sql = """ 
    INSERT INTO verification_code (email, code, created_at, used, ip_address) VALUES (%s, %s, %s, %s, %s)
    """

    try:
        光标.execute(sql, (email, 验证码, 当前时间, 0, IP,))
        连接.commit()
    except Exception as e:
        连接.rollback()
        print("ERROR 验证码在写入到SQL时出现问题")
    finally:
        关闭数据库(连接, 光标)


