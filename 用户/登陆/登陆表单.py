from pydantic import BaseModel


class 登陆表单(BaseModel):
    用户名: str
    密码: str
    two_fa: str