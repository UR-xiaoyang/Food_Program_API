from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from 用户.个人中心.查询信息 import 查询个人信息
from 用户.登陆.登陆令牌 import 验证令牌
from fastapi.encoders import jsonable_encoder

个人信息查询 = APIRouter()
安全 = HTTPBearer()

@个人信息查询.post("/data_find")
async def 信息查询(请求: Request, credentials: HTTPAuthorizationCredentials = Depends(安全)):
    token = credentials.credentials
    令牌信息 = 验证令牌(token)

    if 令牌信息:
        用户信息 = 查询个人信息(令牌信息['sub'])
        json_用户信息 = jsonable_encoder(用户信息)
        if 用户信息:
            raise HTTPException(status_code=200, detail=json_用户信息)
        else:
            raise HTTPException(status_code=404, detail="没有该用户的信息")
    else:
        raise HTTPException(status_code=403, detail="无效的token，请重新登录")
