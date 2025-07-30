import time
import functools
import requests
from logging import getLogger
import traceback


logger = getLogger(__name__)


def retry_decorator(retries=3, delay=10, exceptions=(Exception,)):
    """
    重试装饰器，用于包裹可能需要多次尝试才能成功的函数。
    参数:
        retries (int): 最多重试次数，默认为3次。
        delay (int): 每次重试之间的延迟时间（秒），默认为2秒。
        backoff (int): 延迟的倍数，在每次重试后增加延迟时间， 默认为2。
        exceptions (tuple): 需要捕获并触发重试的异常类型，默认是所有异常。
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            m_retries, m_delay = retries, delay
            while m_retries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    m_retries -= 1
                    print(f'{func.__name__} failed with {e}, Retrying in {m_delay} seconds...')
                    time.sleep(m_delay)
            # 最后一次尝试不等待
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_model_config(config_url, model_name):
    """
    根据模型名称获取模型配置
    """
    payload = {"modelName": model_name}
    try:
        response = requests.post(config_url, json=payload)
        response.raise_for_status()
        result = response.json()
        if result.get("success") and len(result.get("data")) == 1:
            new_api_key = result.get("data")[0]["apiKey"]
            print("模型配置查询成功")
            return new_api_key
        else:
            logger.error(f"模型 {model_name} 配置查询失败: {result}")
            raise Exception("模型配置查询失败")
    except Exception as e:
        logger.error(f"调用模型配置查询接口失败: {str(e)} \n {traceback.format_exc()}")
        raise Exception("模型配置查询失败")