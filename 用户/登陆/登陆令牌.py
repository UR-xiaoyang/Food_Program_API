import json

from pydantic import BaseModel
import jwt as pyjwt
from datetime import datetime, timedelta


# 定义令牌模型
class 令牌Model(BaseModel):
    访问令牌: str
    令牌类型: str
    过期时间: int


def read_config():
    with open("config.json", 'r') as file:
        config = json.load(file)
    return config


SECRET_KEY = read_config().get("jwt_key")


# 生成令牌的函数
def 生成访问令牌(data: dict, 到期时间: int = 720):
    """
    生成JWT访问令牌
    :param data: 包含用户信息的字典
    :param expires_in: 令牌的过期时间，默认30分钟
    :return: 编码后的JWT令牌
    """
    # 设置令牌过期时间
    过期时间 = datetime.utcnow() + timedelta(minutes=到期时间)
    data.update({"exp": 过期时间})

    # 生成访问令牌
    编码JWT = pyjwt.encode(data, SECRET_KEY, algorithm="HS256")

    return 编码JWT


# 验证令牌的函数
def 验证令牌(token: str):
    """
    验证JWT访问令牌的合法性和有效性
    :param token: 要验证的JWT令牌
    :return: 解码后的数据，或None（如果令牌无效）
    """
    try:
        # 解码并验证JWT令牌
        载荷 = pyjwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_signature": True})
        return 载荷
    except pyjwt.ExpiredSignatureError:
        # 处理令牌已过期的错误
        print("令牌已过期")
        return None
    except pyjwt.InvalidTokenError:
        # 处理无效令牌错误
        print("无效的令牌")
        return None


# 调试函数
def Debug():
    """
    用于调试生成和验证令牌的函数
    """
    # 模拟用户数据
    用户数据 = {"username": "test_user", "role": "admin"}

    # 生成访问令牌
    令牌 = 生成访问令牌(用户数据)
    print(f"生成的令牌: {令牌}")

    # 验证令牌
    验证结果 = 验证令牌(令牌)
    if 验证结果:
        print(f"验证成功，用户数据: {验证结果}")
    else:
        print("验证失败")
