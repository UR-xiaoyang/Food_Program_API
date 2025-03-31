from 数据库.联系数据库 import 连接数据库, 关闭数据库


def 查询个人信息(user):
    # 连接数据库
    连接, 光标 = 连接数据库()

    # 寻找用户ID
    寻找ID = """
    SELECT ID FROM user WHERE username = %s
    """
    光标.execute(寻找ID, (user))  # 注意：user是一个变量，传入时需要用元组括起来
    结果 = 光标.fetchone()

    if 结果:
        # 结果是一个元组，ID位于索引0
        user_id = 结果[0]

        寻找ID的信息 = """
        SELECT * FROM users_data WHERE user_id = %s
        """
        光标.execute(寻找ID的信息, (user_id,))  # 传入user_id进行查询
        用户信息 = 光标.fetchone()

        # 关闭数据库连接
        关闭数据库(连接, 光标)
        return 用户信息
    else:
        # 如果没有找到用户ID，关闭数据库连接并返回None
        关闭数据库(连接, 光标)
        return None
