from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from 用户.登陆.登陆令牌 import 验证令牌
from 数据库.联系数据库 import 连接数据库, 关闭数据库
import json

计划内容发送器 = APIRouter()
安全 = HTTPBearer()

@计划内容发送器.post("/send_plan_contents")
async def 发送计划内容(
    plan_id: str,
    token: HTTPAuthorizationCredentials = Depends(安全)
):
    # 验证token并获取用户ID
    令牌信息 = 验证令牌(token.credentials)
    if 令牌信息 is None:
        raise HTTPException(status_code=403, detail="无效的token，请重新登录")
    用户ID = 令牌信息['sub']

    # 连接数据库
    连接, 光标 = 连接数据库()

    try:
        # 将字符串转换为数组
        计划ID列表 = json.loads(plan_id)
        计划内容 = []

        # 获取每个计划的内容
        for 计划ID in 计划ID列表:
            光标.execute("SELECT id, content, is_completed FROM plan_contents WHERE id = %s", (计划ID,))
            内容 = 光标.fetchone()
            if 内容:
                计划内容.append({
                    "id": 内容[0],
                    "text": 内容[1],
                    "完成度": 内容[2]
                })

        return {
            "plan_ids": 计划ID列表,
            "contents": 计划内容
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="无效的plan_id格式")
    except Exception as e:
        连接.rollback()
        raise HTTPException(status_code=500, detail=f"计划内容获取失败: {str(e)}")
    finally:
        关闭数据库(连接, 光标)