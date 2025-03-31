import json
import asyncio

from 数据库.数据库配置 import Config
from 数据库.联系数据库 import 连接数据库, 关闭数据库
from 用户.邮箱.smtp配置 import smtp配置
from 用户.邮箱.SMTP import SMTP
from 计划.计划生成器.GLM import chat
from 计划.计划生成器.GLM_config import GLM配置

from AI.deepseek_config import DeepSeekConfig
def 获取版本号():
    print("v20250329")


def 加载配置():
    with open('config.json') as f:
        return json.load(f)


async def 读取消息():
    messages = [{"role": "user", "content": "我希望回答您好，我是GLM4大模型，很高兴是为你服务"}]
    async for 回答 in chat(messages):
        print(回答, end="")


def 初始化():
    print(">启动SERVER")
    获取版本号()
    配置 = 加载配置()
    print("服务器启动在:", 配置["host"] + ":" + str(配置["port"]))
    print("工作进程数量:", 配置["workers"])
    print("数据库服务器地址:", 配置["SQL_config"]["db_host"])
    print("数据库名称:", 配置["SQL_config"]["db_name"])
    Config.HOST = 配置["SQL_config"]["db_host"]
    Config.NAME = 配置["SQL_config"]["db_name"]
    Config.USER = 配置["SQL_config"]["db_user"]
    Config.PASSWORD = 配置["SQL_config"]["db_password"]
    Config.PORT = 配置["SQL_config"]["db_port"]
    smtp配置.SMTP用户 = 配置["MAIL_config"]["smtp_server_user"]
    smtp配置.SMTP_token = 配置["MAIL_config"]["smtp_server_token"]
    smtp配置.SMTP服务器 = 配置["MAIL_config"]["smtp_server"]
    smtp配置.SMTP端口 = 配置["MAIL_config"]["smtp_server_port"]
    print(f"SMTP服务器:{smtp配置.SMTP服务器}:{smtp配置.SMTP端口}")
    print(f"发信邮箱:{smtp配置.SMTP用户}")
    GLM配置.model = 配置["GLM"]["model"]
    GLM配置.api_key = 配置["GLM"]["api"]
    
    # DeepSeek配置
    DeepSeekConfig.model = 配置["deepseek"]["model"]
    DeepSeekConfig.api_key = 配置["deepseek"]["key"]

    # 数据库测试
    try:
        数据库连接请求, cursor = 连接数据库()
        print("数据库连接成功！")
        关闭数据库(数据库连接请求, cursor)
    except:
        print("数据库连接失败！")
        
    # SMTP服务测试
    try:
        SMTP(配置["MAIL_config"]["test_email"], "食程计划服务端，SMTP服务正常运行！", "食程计划初始化测试", "server")
        print("SMTP测试成功")
    except:
        print("SMTP测试失败")
        # exit()

    # GLM通信
    try:
        print("===GLM===")
        asyncio.run(读取消息())
        print("\n")
    except Exception as e:
        print("GLM初始化失败：" + str(e))
    return 配置

