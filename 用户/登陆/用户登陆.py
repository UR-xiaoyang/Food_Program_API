import pyotp

from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库, 关闭数据库
import bcrypt

def 用户登录(用户名, 密码, IP, two_fa):
    try:
        # 连接到数据库
        数据库连接, cursor = 连接数据库()

        # 查询用户信息
        cursor.execute("SELECT ID, username, password, 2fa_key FROM user WHERE username = %s", (用户名,))
        用户数据 = cursor.fetchone()

        # 如果找到了用户
        if 用户数据:
            # 验证密码
            用户密码 = 用户数据[2].encode('utf-8')  # 修改这里，使用索引访问元组
            two_fa验证码 = pyotp.TOTP(用户数据[3].encode('utf-8'))
            密码验证 = bcrypt.checkpw(密码.encode('utf-8'), 用户密码)
            two_fa验证 = two_fa验证码.verify(two_fa)
            if 密码验证 and two_fa验证:
                # 登录成功
                记录日志(f"{用户名}登陆系统", IP, 用户名)
                return f"登录成功，欢迎 {用户名}!"
            else:
                # 密码错误
                记录日志(f"{用户名}登陆失败，请检查登录信息", IP, 用户名)
                return "密码错误，请重试。"
        else:
            # 用户名不存在
            记录日志(f"{IP}试图使用不存在的用户名“{用户名}”登陆登陆系统", IP, "Login")
            return "用户名错误，请重试。"

    except Exception as e:
        # 如果发生错误，打印错误信息
        print(f"登录系统发生错误: {e}，请联系管理员。")
        return "登录过程中发生错误，请稍后再试。"
    finally:
        # 关闭数据库连接
        关闭数据库(数据库连接, cursor)


#Debug = 用户登录("Debug1", "1234567", "127.0.0.1")
#print(Debug)
