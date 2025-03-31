from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from 用户.个人中心.写入表单 import 个人信息表单
from 用户.个人中心.写入信息 import 更新个人信息

from 用户.登陆.登陆令牌 import 验证令牌

个人信息写入 = APIRouter()
安全 = HTTPBearer()


@个人信息写入.post("/data_write")
async def 信息写入(请求: Request, 表单:个人信息表单, credentials: HTTPAuthorizationCredentials = Depends(安全)):
    IP = 请求.client.host
    token = credentials.credentials
    令牌信息 = 验证令牌(token)
    if 令牌信息:
        用户信息 = 更新个人信息(表单.ID, 表单.年龄, 表单.性别, 表单.体重, 表单.身高, 表单.健康状态, 表单.饮食偏好)
        if 用户信息 is None:
            raise HTTPException(status_code=200, detail="修改成功")
        else:
            raise HTTPException(status_code=404, detail="没有该用户的信息")
    else:
        raise HTTPException(status_code=403, detail="无效的token，请重新登录")