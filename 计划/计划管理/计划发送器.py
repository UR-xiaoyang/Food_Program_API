from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from 用户.登陆.登陆令牌 import 验证令牌
from 数据库.联系数据库 import 连接数据库, 关闭数据库
import json

计划发送器 = APIRouter()
安全 = HTTPBearer()

@计划发送器.post("/send_plan")
async def 发送计划(
    token: HTTPAuthorizationCredentials = Depends(安全)
):
    # 验证token并获取用户ID
    令牌信息 = 验证令牌(token.credentials)
    if 令牌信息 is None:
        raise HTTPException(status_code=403, detail="无效的token，请重新登录")
    发送者 = 令牌信息['sub']

    # 连接数据库
    连接, 光标 = 连接数据库()

    try:
        # 获取计划信息
        光标.execute("SELECT * FROM plans WHERE user_id = %s", (发送者,))
        计划信息列表 = 光标.fetchall()
        if not 计划信息列表:
            raise HTTPException(status_code=404, detail="计划未找到")
        
        # 返回json
        return [
            {
                "plan_id": 计划信息[0],
                "plan_name": 计划信息[1],
                "plan_time": 计划信息[2],
                "paln_content_id": 计划信息[3],
            }
            for 计划信息 in 计划信息列表
        ]
    except Exception as e:
        连接.rollback()
        raise HTTPException(status_code=500, detail=f"计划发送失败: {str(e)}")
    finally:
        关闭数据库(连接, 光标)