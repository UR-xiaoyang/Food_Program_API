from pydantic import BaseModel
from decimal import Decimal

class 个人信息表单(BaseModel):
    ID: int
    年龄: int
    性别: str
    体重: Decimal
    身高: Decimal
    健康状态: str
    饮食偏好: str