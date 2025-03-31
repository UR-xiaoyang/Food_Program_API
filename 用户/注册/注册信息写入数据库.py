from 数据库.日志.log表 import 记录日志
from 数据库.联系数据库 import 连接数据库, 关闭数据库
import bcrypt
import pyotp
# 生成随机密钥

def 注册写入数据库(用户名, 密码, 邮箱, IP):
    try:
        # 连接到数据库
        数据库连接, cursor = 连接数据库()

        # 对密码进行哈希处理
        hash加密密码 = bcrypt.hashpw(密码.encode('utf-8'), bcrypt.gensalt())

        # 预生成2FA密钥
        随机密钥 = pyotp.random_base32()

        # 执行SQL插入操作
        cursor.execute(
            "INSERT INTO user (username, password, email, 2fa_key) VALUES (%s, %s, %s, %s)",
            (用户名, hash加密密码, 邮箱, 随机密钥))
        # 生成

        # 获取ID
        用户ID = cursor.lastrowid

        # 提交事务
        数据库连接.commit()

        # 增加users_data表
        cursor.execute("INSERT INTO users_data (user_id) VALUES (%s)", (用户ID,))
        # 增加nutrition_data表
        cursor.execute("""
            INSERT INTO nutrition_data 
            (user_id, protein, carbohydrates, fat, fiber, vitamin_c) 
            VALUES (%s, 0, 0, 0, 0, 0)
        """, (用户ID,))
        数据库连接.commit()
        记录日志("注册成功", IP, 用户名)
        return 随机密钥
    except Exception as e:
        # 如果发生错误，打印错误信息
        print(f"注册写入数据库时发生错误: {e}")
    finally:
        # 关闭数据库连接
        关闭数据库(数据库连接, cursor)


# 调用函数示例
#def debug():
#    注册写入数据库("Debug", "123456", "test@test.com", "666", "天地银行", "测试用户", "测试部门", "127.0.0.1")
#debug()
