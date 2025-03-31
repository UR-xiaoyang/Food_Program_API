from 数据库.联系数据库 import 连接数据库, 关闭数据库


def 更新个人信息(ID, 年龄, 性别, 体重, 身高, 健康状态, 饮食偏好):
    try:
        更新语句 = """
        UPDATE users_data SET age = %s , gender = %s , weight = %s , height = %s , health_status = %s , diet_preference = %s WHERE id = %s
        """
        连接, 光标 = 连接数据库()
        光标.execute(更新语句, (年龄, 性别, 体重, 身高, 健康状态, 饮食偏好, ID))
        连接.commit()
        关闭数据库(连接, 光标)
    except Exception as e:
        print(e)
        return e