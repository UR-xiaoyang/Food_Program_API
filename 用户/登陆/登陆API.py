from fastapi import APIRouter, HTTPException, Request
from 用户.登陆.用户登陆 import 用户登录
from 用户.登陆.登陆令牌 import 生成访问令牌
from 用户.登陆.登陆表单 import 登陆表单

登陆路由 = APIRouter()


@登陆路由.post("/sign_in")
async def 登陆API(请求: Request, 表单: 登陆表单):
    登录结果 = 用户登录(表单.用户名, 表单.密码, 请求.client.host, 表单.two_fa)

    # 处理登录结果
    if "登录成功" in 登录结果:
        # 登录成功时，生成访问令牌
        生成令牌 = 生成访问令牌(data={"sub": 表单.用户名})
        return {
            "access_token": 生成令牌,
            "token_type": "bearer",
            "username": 表单.用户名
        }
    else:
        # 如果登录失败，抛出对应的错误信息
        raise HTTPException(status_code=400, detail=登录结果)
