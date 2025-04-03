from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# 导入模块（保持不变）
from 初始化 import 初始化
from 用户.个人中心.写入API import 个人信息写入
from 用户.个人中心.查询API import 个人信息查询
from 用户.注册.注册API import 注册路由
from 用户.登陆.登陆API import 登陆路由
from 用户.注册.验证码API import 验证码
from 计划.计划生成器.GLM_API import GLM
from 计划.计划生成器.计划提交 import 计划提交
from 计划.计划管理.计划发送器 import 计划发送器
from 计划.计划管理.计划内容发送器 import 计划内容发送器
from 计划.计划管理.计划更新器 import 计划更新器
from 计划.计划管理.用户营养数据发送器 import 营养数据发送器

# 初始化
配置 = 初始化()
app = FastAPI()

# CORS 配置（保持不变）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由（保持不变）
app.include_router(注册路由, prefix="/user")
app.include_router(登陆路由, prefix="/user")
app.include_router(验证码, prefix="/user")
app.include_router(个人信息查询, prefix="/user")
app.include_router(个人信息写入, prefix="/user")
app.include_router(GLM, prefix="/user")
app.include_router(计划提交, prefix="/plan")
app.include_router(计划发送器, prefix="/plan")
app.include_router(计划内容发送器, prefix="/plan")
app.include_router(计划更新器, prefix="/plan")
app.include_router(营养数据发送器, prefix="/plan")

# OPTIONS 请求处理（保持不变）
@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    response = JSONResponse({"message": "CORS preflight"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

if __name__ == "__main__":
    # 仅在开发时运行 Uvicorn
    uvicorn.run("main:app", host=配置["host"], port=配置["port"], workers=配置["workers"], reload=False)
