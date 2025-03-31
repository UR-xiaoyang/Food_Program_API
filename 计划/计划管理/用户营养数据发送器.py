from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from 用户.登陆.登陆令牌 import 验证令牌
from 数据库.联系数据库 import 连接数据库, 关闭数据库
import json

营养数据发送器 = APIRouter()
安全 = HTTPBearer()

@营养数据发送器.post("/send_nutrition_data")
async def 发送营养数据(
    token: HTTPAuthorizationCredentials = Depends(安全)
):
    # 验证token并获取用户ID
    令牌信息 = 验证令牌(token.credentials)
    if 令牌信息 is None:
        raise HTTPException(status_code=403, detail="无效的token，请重新登录")
    用户 = 令牌信息['sub']

    # 连接数据库
    连接, 光标 = 连接数据库()
    try:
        # 查询用户的id
        查询语句 = "SELECT id FROM user WHERE username = %s"
        光标.execute(查询语句, (用户,))
        用户id = 光标.fetchone()
        # 从数据库中获取用户的营养数据信息
        查询语句 = "SELECT protein, carbohydrates, fat, fiber, vitamin_c FROM nutrition_data WHERE user_id = %s"
        光标.execute(查询语句, (用户id,))
        营养数据 = 光标.fetchone()

        if not 营养数据:
            raise HTTPException(status_code=404, detail="未找到该用户的营养数据")
        
        # 格式化返回数据
        返回数据 = {
            "protein": 营养数据[0],
            "carbohydrates": 营养数据[1],
            "fat": 营养数据[2],
            "fiber": 营养数据[3],
            "vitamin_c": 营养数据[4]
        }

        return {"status": "success", "data": 返回数据}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取营养数据时出错: {str(e)}")
    finally:
        关闭数据库(连接, 光标)
