from enum import Enum
from logging import getLogger
import time
import traceback
from typing import Any
from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from hk_ai_common.http.contextvar import ContentVarKey, trace_id_context, task_id_context

logger = getLogger(__name__)
TRACE_ID_KEY = ContentVarKey.TRACE_ID_KEY.value  # 链路id上下文键
TASK_ID_KEY = ContentVarKey.TASK_ID_kEY


# 异常码
class ErrorCode(Enum):
	# 执行成功
	OK = "00000"
	# 业务异常，例如：用户不存在
	WARN = "00400"
	# 请求参数错误
	PARAMS_ERROR = "00100"
	# 资源不存在，例如：用户不存在
	NOT_FOUND = "00404"
	# 未知系统异常
	ERROR = "00500"
	# 自定义错误码
	# 照片推理失败
	INFERENCE_FAILED = "1000400600"
	# 形象照片不合法
	IMAGE_PHOTOS_ARE_ILLEGAL = "1000400601"


def create_json_response(data: Any = {}, message="成功", status="00000", success=True, headers=None,
						 status_code: int = 200):
	"""
	创建json响应对象
	"""
	return JSONResponse(
		content={
			"data": jsonable_encoder(data),
			"message": message,
			"status": status,
			"success": success,
			'trace_id': str(trace_id_context.get(TRACE_ID_KEY)),
			'taskId': str(task_id_context.get(TASK_ID_KEY))
		},
		headers=headers,
		status_code=status_code
	)


# 业务异常类
class BusinessError(Exception):
	"""
	业务异常类型
	"""

	def __init__(self, errMsg: str, errCode: ErrorCode = ErrorCode.WARN, headers=None):
		self.errMsg = errMsg
		self.errCode = errCode
		self.headers = headers


# 初始化异常拦截器
def init_exception_handler(app: FastAPI):
	"""
	初始化异常拦截器
	- 统一异常处理
	- 统一请求日志打印
	"""

	@app.middleware('http')
	async def catch_exception(request: Request, call_next):
		# 请求到达时打印日志
		start_time = time.time()
		method = request.method
		url = str(request.url)
		logger.info(f"Request received: {method} {url}")
		response = None
		# 处理请求
		try:
			response = await call_next(request)
		except RequestValidationError as e:
			raise e
		except Exception as e:
			logger.error(f"{e}\n{traceback.format_exc()}")
			response = create_json_response(success=False, status=ErrorCode.ERROR.value, message='服务器未知异常')
		finally:
			# 请求结束后打印日志
			# 请求结束后打印日志
			status_code = None
			process_time = time.time() - start_time
			if response is not None:
				status_code = response.status_code
				response.headers["X-Process-Time"] = str(process_time)
			logger.info(
				f"Request processed: {method} {url} - Status Code: {status_code} - Process Time: {process_time:.4f}s")
			return response

	# 参数异常
	@app.exception_handler(RequestValidationError)
	async def request_validation_exception_handler(
			request: Request, exc: RequestValidationError
	) -> JSONResponse:
		# 格式化错误信息，使其可序列化
		formatted_errors = []
		for error in exc.errors():
			formatted_error = {
				"loc": error["loc"],  # 错误位置
				"msg": error["msg"],  # 错误消息
				"type": error["type"],  # 错误类型
			}
			formatted_errors.append(formatted_error)
		formatted_errors_json = jsonable_encoder(formatted_error)
		logger.info(f"{RequestValidationError.__name__}：{formatted_errors_json}")
		return create_json_response(success=False, status=ErrorCode.PARAMS_ERROR.value, message='请求参数错误',
									data=formatted_errors_json)

	# 业务异常处理
	@app.exception_handler(BusinessError)
	async def business_error_handler(request: Request, exc: BusinessError) -> Response:
		logger.warning(f"{BusinessError.__name__}:{exc.errMsg}\n{traceback.format_exc()}")
		return create_json_response(success=False, status=exc.errCode.value, message=exc.errMsg)
