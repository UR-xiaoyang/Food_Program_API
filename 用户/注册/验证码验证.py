from 数据库.联系数据库 import 连接数据库, 关闭数据库
from datetime import datetime, timedelta

def 验证码验证(邮箱, 前端输入验证码):
    连接, 光标 = 连接数据库()
    try:
        SQL = """
        SELECT email,created_at FROM verification_code WHERE code = %s AND used = '0' ORDER BY ID DESC LIMIT 1;
        """
        光标.execute(SQL, (前端输入验证码,))
        数据 = 光标.fetchone()
        if 数据:
            if 数据[0] == 邮箱 and datetime.now() - 数据[1] < timedelta(minutes=1):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        return e
    finally:
        关闭数据库(连接, 光标)

