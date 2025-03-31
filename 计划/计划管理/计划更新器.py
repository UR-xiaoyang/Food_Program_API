from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from 数据库.联系数据库 import 连接数据库, 关闭数据库
from 用户.登陆.登陆令牌 import 验证令牌
import json
# 导入 Pydantic 和 typing
from pydantic import BaseModel
from typing import List
import uuid as py_uuid # 建议导入并重命名，以防和变量名冲突

计划更新器 = APIRouter()
安全 = HTTPBearer()

# 定义输入数据模型
class PlanContentUpdate(BaseModel):
    uuid: str # 可以考虑使用 py_uuid.UUID 类型进行更严格的验证
    completed: bool

@计划更新器.put("/update_plan_contents")
async def 更新计划内容完成状态(
    updates: List[PlanContentUpdate], # 修改参数类型为 Pydantic 模型列表
    token: HTTPAuthorizationCredentials = Depends(安全)
):
    # 验证token并获取用户ID
    令牌信息 = 验证令牌(token.credentials)
    if 令牌信息 is None:
        raise HTTPException(status_code=403, detail="无效的token，请重新登录")
    
    # 连接数据库
    连接, 光标 = 连接数据库()
    
    # 通过username获取用户ID
    光标.execute(
        "SELECT id FROM user WHERE username = %s",
        (令牌信息['sub'],)
    )
    用户信息 = 光标.fetchone()
    if not 用户信息:
        raise HTTPException(status_code=404, detail="用户不存在")
    用户ID = 用户信息[0]

    try:
        # 批量更新计划内容完成状态
        for item in updates: # 遍历解析后的对象列表
            # 先查询当前完成状态
            光标.execute(
                "SELECT is_completed FROM plan_contents WHERE id = %s",
                (item.uuid,)
            )
            当前状态 = 光标.fetchone()
            
            # 只有当状态确实改变时才处理营养数据
            if 当前状态 and (当前状态[0] != item.completed):
                # 检索item.uuid对应的plan_nutrition表中的营养值
                光标.execute(
                    "SELECT protein, carbohydrates, fat, fiber, vitamin_c FROM plan_nutrition WHERE plan_contents_uuid = %s",
                    (item.uuid,)
                )
                营养 = 光标.fetchone()
                
                # 更新plan_contents表
                光标.execute(
                    "UPDATE plan_contents SET is_completed = %s WHERE id = %s",
                    (item.completed, item.uuid,) # 使用 Pydantic 模型的属性
                )
                
                # 更新nutrition_data表
                if 营养:
                    系数 = 1 if item.completed else -1  # 根据新状态决定加减
                    光标.execute(
                        """UPDATE nutrition_data 
                        SET protein = protein + (%s * %s),
                            carbohydrates = carbohydrates + (%s * %s),
                            fat = fat + (%s * %s),
                            fiber = fiber + (%s * %s),
                            vitamin_c = vitamin_c + (%s * %s)
                        WHERE user_id = %s""",
                        (营养[0], 系数, 营养[1], 系数, 营养[2], 系数, 
                         营养[3], 系数, 营养[4], 系数, 用户ID)
                    )
            else:
                # 如果状态没有改变，直接更新plan_contents表
                光标.execute(
                    "UPDATE plan_contents SET is_completed = %s WHERE id = %s",
                    (item.completed, item.uuid,)
                )
            # 先查询当前完成状态
            光标.execute(
                "SELECT is_completed FROM plan_contents WHERE id = %s",
                (item.uuid,)
            )
            当前状态 = 光标.fetchone()
            
            # 只有当状态确实改变时才处理营养数据
            if 当前状态 and (当前状态[0] != item.completed):
                # 检索item.uuid对应的plan_nutrition表中的营养值
                光标.execute(
                    "SELECT protein, carbohydrates, fat, fiber, vitamin_c FROM plan_nutrition WHERE plan_contents_uuid = %s",
                    (item.uuid,)
                )
                营养 = 光标.fetchone()
                
                # 更新nutrition_data表
                if 营养:
                    系数 = 1 if item.completed else -1  # 根据新状态决定加减
                    光标.execute(
                        """UPDATE nutrition_data 
                        SET protein = protein + (%s * %s),
                            carbohydrates = carbohydrates + (%s * %s),
                            fat = fat + (%s * %s),
                            fiber = fiber + (%s * %s),
                            vitamin_c = vitamin_c + (%s * %s)
                        WHERE user_id = %s""",
                        (营养[0], 系数, 营养[1], 系数, 营养[2], 系数, 
                         营养[3], 系数, 营养[4], 系数, 用户ID)
                    )
            

        # 提交事务
        连接.commit()
        return {"message": "计划内容状态更新成功"}

    except Exception as e:
        # 回滚事务
        连接.rollback()
        raise HTTPException(status_code=500, detail=f"计划内容状态更新失败: {str(e)}")
    finally:
        关闭数据库(连接, 光标)