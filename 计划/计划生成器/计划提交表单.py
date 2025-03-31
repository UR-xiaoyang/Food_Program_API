from pydantic import BaseModel


class 计划提交表单(BaseModel):
    标题: str
    时间: str
    计划步骤内容列表: list[str]