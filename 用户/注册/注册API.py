from fastapi import APIRouter, HTTPException, Request
from 用户.注册.注册表单 import 注册表单
from 用户.注册.注册验证 import 注册验证

注册路由 = APIRouter()


@注册路由.post("/sign_up")
async def 注册API(请求: Request, 表单: 注册表单):
    IP = 请求.client.host
    注册结果 = 注册验证(表单.用户名, 表单.密码, 表单.邮箱, 表单.验证码, IP)
    if 注册结果 == "验证码错误" or 注册结果 == "用户存在":
        raise HTTPException(status_code=409, detail=注册结果)
    else:
        raise HTTPException(status_code=200, detail=注册结果)
