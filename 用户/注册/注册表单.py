from pydantic import BaseModel

class 注册表单(BaseModel):
    用户名: str
    密码: str
    邮箱: str
    验证码: str