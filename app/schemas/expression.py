from pydantic import BaseModel


class ExpressionRequest(BaseModel):
    expr: str
    diff_var: str


class ExpressionResponse(BaseModel):
    derivative: str
    img_path: str
