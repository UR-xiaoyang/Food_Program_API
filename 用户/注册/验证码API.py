from fastapi import APIRouter, HTTPException, Request

from 用户.注册.发送验证码 import 发送验证码, 生成验证码, 邮箱冷却

验证码 = APIRouter()

@验证码.post("/mail_code")
async def 验证码API(请求: Request, 邮箱:str):
    IP = 请求.client.host
    验证冷却 = 邮箱冷却(邮箱)
    if not 验证冷却:
        raise HTTPException(status_code=403, detail="请1分钟后再次尝试")
    验证码 = 生成验证码()

    结果 = 发送验证码(邮箱, 验证码, IP)
    if "发送成功" in 结果:
        raise HTTPException(status_code=200, detail="验证码发送成功")
    else:
        raise HTTPException(status_code=500, detail=f"验证码发送失败,{结果}")
