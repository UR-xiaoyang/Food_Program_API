from fastapi import APIRouter, Request, Query, Depends
from fastapi.responses import StreamingResponse
import json

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pymysql import NULL

from 用户.个人中心.查询信息 import 查询个人信息
from 用户.登陆.登陆令牌 import 验证令牌
from 计划.计划生成器.GLM import chat
from datetime import datetime

async def 计算营养值(plan_content: str):
    # 获取服务器当前时间
    server_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 定义系统消息模板
    txt1 = f"""
    你是一个营养师，你需要为计划内容计算详细的营养值，
    当前服务器时间：{server_time}
    """
    txt2 = """
    计划内容:
    {plan_content}

    请按照以下格式返回营养值计算结果:
    @nutrition[
        !title = "营养分析";
        !total_calories = 总卡路里(千卡);
        !protein = 蛋白质(g);
        !carbohydrate = 碳水化合物(g);
        !fat = 脂肪(g);
        !fiber = 纤维素(g);
        !vitamin_c = 维生素C(mg);
        !id = 分析ID;
    ]noitirtun@
    """
    SYSTEM_MESSAGE_TEMPLATE = txt1 + txt2.format(plan_content=plan_content)

    # 创建系统消息
    system_message = {
        "role": "system",
        "content": SYSTEM_MESSAGE_TEMPLATE
    }

    # 创建用户消息
    user_message = {
        "role": "user",
        "content": f"请分析以下计划的营养值: {plan_content}"
    }

    # 调用 chat 函数并处理结果
    response = ""
    async for chunk in chat([system_message, user_message]):
        response += chunk
    
    # 解析营养分析结果
    try:
        start = response.find("@nutrition[")
        end = response.find("]noitirtun@")
        if start == -1 or end == -1:
            raise ValueError("无法解析营养分析结果")
        
        nutrition_data = {}
        content = response[start+11:end]
        for line in content.split(";"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("!"):
                key, value = line[1:].split("=", 1)
                nutrition_data[key.strip()] = value.strip()
        
        def 获取数值(key):
            try:
                return float(nutrition_data.get(key, "0").split("(")[0])
            except:
                return 0.0
        
        return {
            "总卡路里": 获取数值("total_calories"),
            "蛋白质": 获取数值("protein"),
            "碳水化合物": 获取数值("carbohydrate"),
            "脂肪": 获取数值("fat"),
            "纤维素": 获取数值("fiber"),
            "维生素C": 获取数值("vitamin_c")
        }
    except Exception as e:
        return ValueError(f"解析营养数据失败: {str(e)}")