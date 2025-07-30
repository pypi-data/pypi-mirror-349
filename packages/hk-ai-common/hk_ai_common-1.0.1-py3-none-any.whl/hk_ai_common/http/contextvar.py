import contextvars
from enum import Enum


class ContentVarKey(Enum):
    """上下文变量key枚举"""
    TRACE_ID_KEY =  "trace-id" # 链路id
    ALG_SERVICE_CODE = "alg-service-code"
    TASK_ID_kEY = "task-id"

trace_id_context = contextvars.ContextVar(ContentVarKey.TRACE_ID_KEY.value, default="-")
trace_id_context.set("-")

alg_service_code_context = contextvars.ContextVar(ContentVarKey.ALG_SERVICE_CODE.value, default="-")
alg_service_code_context.set("-")

task_id_context = contextvars.ContextVar(ContentVarKey.TASK_ID_kEY.value, default="-")
task_id_context.set("-")