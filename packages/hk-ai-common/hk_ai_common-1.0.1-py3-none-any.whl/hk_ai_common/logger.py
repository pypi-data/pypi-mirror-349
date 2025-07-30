import json
import logging.config
import os
import threading
import traceback
import uuid
from logging import Filter, getLogger
from fastapi import FastAPI, Request, Response
import builtins

from date import format_datetime_with_timezone
from hk_ai_common.http.contextvar import ContentVarKey, trace_id_context, alg_service_code_context, task_id_context

TRACE_ID_KEY = ContentVarKey.TRACE_ID_KEY.value  # 链路id上下文键
X_TRACE_ID_KEY = 'X-Trace-ID'  # 链路id请求头键
X_ALG_SERVICE_CODE_KEY = 'X-Alg-Service-Code'  # 算法服务code请求头键
X_TASK_ID_KEY = 'X-Task-ID'

log_colors = {
    'DEBUG': '\033[34m',  # 蓝色
    'INFO': '\033[32m',  # 绿色
    'WARNING': '\033[33m',  # 黄色
    'ERROR': '\033[31m',  # 红色
    'CRITICAL': '\033[41m',  # 红色背景
    'RESET': '\033[0m'  # 重置颜色
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        original_message = super().format(record)
        color = log_colors.get(record.levelname, log_colors['RESET'])
        reset = log_colors['RESET']
        levelname = f"{color}{record.levelname}{reset}"
        # 替换 levelname 部分
        return original_message.replace(record.levelname, levelname)


format = '%(asctime)s %(levelname)s\tpid:%(process)d tid:%(thread)d [%(trace_id)s] %(name)s %(message)s %(pathname)s:%(lineno)d'

formatter = ColoredFormatter(format)

logging.basicConfig(level=logging.INFO)


class TraceIDFilter(Filter):
    def filter(self, record):
        record.trace_id = trace_id_context.get(TRACE_ID_KEY)
        return True


for handler in logging.root.handlers:
    handler.addFilter(TraceIDFilter())
    handler.setFormatter(formatter)

old_print = builtins.print


def custom_print(*args, **kwargs):
    """
    自定义的 print 函数
    """
    try:
        # 将 trace_id 添加到输出内容的前面
        trace_id = trace_id_context.get("trace-id")
        if trace_id is None:
            trace_id = "-"

        # 格式化时间
        formatted_time = format_datetime_with_timezone()[:-3]

        # 进程id
        pid = os.getpid()
        # 线程id
        tid = threading.get_ident()
        old_print(
            f"{formatted_time} {log_colors.get('INFO')}PRINT{log_colors.get('RESET')}\tpid:{pid} tid:{tid} [{trace_id}]",
            *args, **kwargs)
    except Exception as e:
        old_print(e)


# 替换内置的 print 函数
builtins.print = custom_print

logger = getLogger(__name__)


def init_log(app: FastAPI):
    """
    初始化日志打印
    - 日志格式化
    - 日志traceId
    - 日志串联X-Trace-ID
    - 重写print
    """

    @app.middleware("http")
    async def extra_process(request: Request, call_next):
        trace_id = request.headers.get(X_TRACE_ID_KEY, None)
        if trace_id is None:
            # 获取链路id
            try:
                body = json.loads(await request.body())
                if 'trace_id' in body:
                    trace_id = body['trace_id']
            except json.JSONDecodeError:
                logger.warning('[json解析失败] body提取trace_id失败')
            except Exception as e:
                logger.warning(f"[提取trace_id失败] {e}\n{traceback.format_exc()}")
        if trace_id is None:
            trace_id = uuid.uuid4().hex
        trace_id_context.set(trace_id)

        alg_service_code = request.headers.get(X_ALG_SERVICE_CODE_KEY, None)
        if alg_service_code is None:
            # 获取算法code
            try:
                body = json.loads(await request.body())
                if 'algServiceCode' in body:
                    alg_service_code = body['algServiceCode']
            except json.JSONDecodeError:
                logger.warning('[json解析失败] body提取algServiceCode失败')
            except Exception as e:
                logger.warning(f"[提取algServiceCode失败] {e}\n{traceback.format_exc()}")
        if alg_service_code is None:
            alg_service_code = ""
        alg_service_code_context.set(alg_service_code)

        task_id = request.headers.get(X_TASK_ID_KEY, None)
        if task_id is None:
            # 获取task_id
            try:
                body = json.loads(await request.body())
                if 'taskId' in body:
                    task_id = body['taskId']
            except json.JSONDecodeError:
                logger.warning('[json解析失败] body提取taskId失败')
            except Exception as e:
                logger.warning(f"[提取taskId失败] {e}\n{traceback.format_exc()}")
        if task_id is None:
            task_id = ""
        task_id_context.set(task_id)

        response: Response = await call_next(request)

        response.headers[X_TRACE_ID_KEY] = trace_id

        trace_id_context.set("-")
        alg_service_code_context.set("-")
        task_id_context.set("-")

        return response
