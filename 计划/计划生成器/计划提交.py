from fastapi import APIRouter, HTTPException, Depends
from uuid import uuid4
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from 用户.登陆.登陆令牌 import 验证令牌
from 数据库.联系数据库 import 连接数据库, 关闭数据库
import json
from 计划.计划生成器.计划提交表单 import 计划提交表单
from 计划.计划生成器.计划营养值计算器 import 计算营养值

计划提交 = APIRouter()
安全 = HTTPBearer()

@计划提交.post("/submit_plan")
async def 提交计划(
    表单: 计划提交表单,
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
        步骤内容ID = []
        连接.begin()  # 显式开启事务
        # 插入计划步骤内容到plan_contents表
        for 步骤内容 in 表单.计划步骤内容列表:
            新UUID = str(uuid4())
            光标.execute("SELECT id FROM plan_contents WHERE id = %s", (新UUID,))
            if not 光标.fetchone():
                光标.execute(
                    "INSERT INTO plan_contents (ID, content, is_completed) VALUES (%s, %s, %s)",
                    (新UUID, 步骤内容, False)
                )
                营养值 = await 计算营养值(步骤内容)
                # 写入营养值到plan_nutrition表，plan_contents_uuid为新UUID，protein，carbohydrates，fat，fiber，vitamin_c
                光标.execute(
                    "INSERT INTO plan_nutrition (plan_contents_uuid, protein, carbohydrates, fat, fiber, vitamin_c) VALUES (%s, %s, %s, %s, %s, %s)",
                    (新UUID, 营养值['蛋白质'], 营养值['碳水化合物'], 营养值['脂肪'], 营养值['纤维素'], 营养值['维生素C']) 
                )    
            步骤内容ID.append(新UUID)
        
        # 插入计划信息到plans表
        光标.execute(
            "INSERT INTO plans (user_id, title, time, data) VALUES (%s, %s, %s, %s)",
            (用户ID, 表单.标题, 表单.时间, json.dumps(步骤内容ID))  # 将列表转换为JSON字符串
        )
        # 提交事务
        连接.commit()
        return {"message": "计划提交成功"}
    except Exception as e:
        # 回滚事务
        连接.rollback()
        raise HTTPException(status_code=500, detail=f"计划提交失败: {str(e)}")
    finally:
        关闭数据库(连接, 光标)