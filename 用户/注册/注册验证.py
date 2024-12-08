from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库, 关闭数据库
from 用户.注册.注册信息写入数据库 import 注册写入数据库
from 用户.注册.验证码验证 import 验证码验证


def 注册验证(用户名, 密码, 邮箱, 验证码, IP):
    # 检验邮箱是否注册
    数据库连接请求, cursor = 连接数据库()
    try:
        验证码正确性 = 验证码验证(邮箱, 验证码)

        if not 验证码正确性:
            记录日志(f"在试图注册“{用户名}”邮箱验证码错误", IP, 用户名)
            return "验证码错误"
        # 连接到数据库


        # 查询用户名是否存在
        cursor.execute("SELECT * FROM user WHERE username = %s", (用户名))
        用户名存在 = cursor.fetchone() is not None
        cursor.execute("SELECT * FROM user WHERE email = %s", (邮箱))
        邮箱存在 = cursor.fetchone() is not None
        # 根据查询结果进行后续处理
        if 用户名存在 or 邮箱存在:
            记录日志(f"{IP}在试图注册已经注册的用户“{用户名}”", IP, "Login")
            return "用户或邮箱存在"
        else:
            two_fa = 注册写入数据库(用户名, 密码, 邮箱, IP)
            return two_fa
        # 查询是否存在相同邮箱

    except Exception as e:
        # 如果发生错误，打印错误信息
        print(f"注册验证过程中发生错误: {e}")
        return "注册验证过程中发生错误，请稍后再试。"
    finally:
        # 关闭数据库连接
        关闭数据库(数据库连接请求, cursor)
