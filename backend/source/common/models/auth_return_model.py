from pydantic import BaseModel
from typing import Dict


class RpcFunctionReturnValue(BaseModel):
    success: bool = True
    return_value: Dict | None = None
    error_code: int | None = None
    error_message: str | None = None