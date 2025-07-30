
from typing import Dict

from pydantic import BaseModel


class AlgRequest(BaseModel):
    taskId: str
    param: Dict

class AlgResponse(BaseModel):
    taskId: str
    code: str
    message: str
    data: Dict