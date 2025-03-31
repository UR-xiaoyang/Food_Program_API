import random
import string
import traceback
from datetime import datetime, timedelta

from 数据库.联系数据库 import 连接数据库, 关闭数据库
from 用户.注册.验证码写入数据库 import 验证码写入
from 用户.邮箱.SMTP import SMTP


def 生成验证码(length=6):
    """
    生成一个6位随机长度的验证码
    """
    验证码 = "".join(random.choices(string.digits, k=length))
    return 验证码


def 发送验证码(收件人, 验证码, IP):
    """
    调用SMTP发送验证码到目标
    """
    try:
        邮件内容 = f"亲爱的用户，这是你的验证码{验证码}"
        邮件主题 = f"您好，亲爱的用户，欢迎您首次注册”食程计划“"
        SMTP(收件人, 邮件内容, 邮件主题, IP)
        验证码写入(收件人, 验证码, IP)
        return "发送成功"
    except Exception as e:
        错误信息 = traceback.format_exc()
        return f"发送失败, 错误信息：{错误信息}"

def 邮箱冷却(收件人):
    global 连接, 光标
    try:
        连接, 光标 = 连接数据库()
        sql = """
        SELECT email,created_at FROM verification_code WHERE email = %s AND used = '0' ORDER BY ID DESC LIMIT 1;
        """

        光标.execute(sql, (收件人,))
        数据 = 光标.fetchone()
        if 数据:
            创建时间 = 数据[1]
            时间差 = datetime.now() - 创建时间
            if 时间差 < timedelta(minutes=1):
                return False
            else:
                return True
        else:
            return True
    except Exception as e:
        return e
    finally:
        关闭数据库(连接, 光标)