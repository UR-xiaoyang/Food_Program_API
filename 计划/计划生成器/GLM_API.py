from fastapi import APIRouter, Request, Query, Depends
from fastapi.responses import StreamingResponse
import json

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pymysql import NULL

from 用户.个人中心.查询信息 import 查询个人信息
from 用户.登陆.登陆令牌 import 验证令牌
from 计划.计划生成器.GLM import chat

from datetime import datetime

GLM = APIRouter()
安全 = HTTPBearer()

@GLM.post("/glm")
async def GLM_stream(request: Request, messages: str = Query(...), credentials: HTTPAuthorizationCredentials = Depends(安全)):
    token = credentials.credentials
    token_data = 验证令牌(token)

    if token_data is None:
        return {"message": "无效的令牌"}

    user_info = 查询个人信息(token_data['sub']) or [NULL,NULL,NULL,NULL]

    # 获取服务器当前时间
    server_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 定义系统消息模板
    txt1 = f"""
    你是一个营养师，你需要为用户提供合适的营养计划，
    这是用户的信息：
    服务器时间：{server_time}
    年龄：{user_info[2]}
    性别：{user_info[3]}
    体重：{user_info[4]}
    身高：{user_info[5]}
    健康状态：{user_info[6]}
    饮食偏好：{user_info[7]}
    """
    txt2 = """
    计划语言:

@plan[
    !title = "计划";
    !time = "执行时间";
    !具体内容 = [计划内容1,计划内容2,...];
    !id = 计划ID; // id是当前对话内的第几个计划
]nalp@


示例：
@plan[
    !title = "健康计划";
    !time = "2024-12-01";
    !具体内容 = [每天跑步30分钟,每周测量体重,每月进行健康检查];
    !id = 1; 
]nalp@

计划必须使用计划语言，结尾必须为nalp@
    """
    SYSTEM_MESSAGE_TEMPLATE = txt1 + txt2

    try:
        messages_list = json.loads(messages)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format for messages."}

    # 创建系统消息
    system_message = {
        "role": "system",
        "content": SYSTEM_MESSAGE_TEMPLATE
    }

    # 将系统消息插入到消息列表的最前面
    messages_list.insert(0, system_message)

    # 调用 chat 函数，假设它返回一个生成器或迭代器
    response_stream = chat(messages_list)

    return StreamingResponse(response_stream, media_type='text/plain')