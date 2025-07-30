import json
import logging
from functools import wraps

from requests.exceptions import ReadTimeout
from django.http import JsonResponse
from bkapi.bk_notice.client import Client

from . import config

# 配置日志记录器
logger = logging.getLogger(__name__)


def return_json_response(view_func):
    """
    将返回的dict数据转为JsonResponse
    @param view_func:
    @return:
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        result = view_func(request, *args, **kwargs)
        # 如果返回的是dict且request中有trace_id，则在响应中加上
        if isinstance(result, dict):
            if hasattr(request, "trace_id"):
                result["trace_id"] = request.trace_id
            result = JsonResponse(result, status=result.pop("code", 200))
        return result

    return _wrapped_view


def api_call(api_method: str, success_message: str, error_message: str, success_code=200, error_code=500, **kwargs):
    """
    向apigw请求并返回客户端解析的结构化结果。
    :param api_method: 调用方法
    :param success_message: 成功信息
    :param error_message: 失败信息
    :param success_code: 成功状态码
    :param error_code: 失败状态码
    :param kwargs:
        data: Request data to sent.
        path_params: Variables parts of the url path.
        params: Variables in the query string.
        headers: HTTP Headers to send.
        timeout: Seconds to wait for the server to send data before giving up.
        proxies: Protocol proxies mappings.
        verify: Should we verify the server TLS certificate.
    """
    headers = {
        "x-bkapi-authorization": json.dumps(
            {"bk_app_code": config.BK_API_APP_CODE, "bk_app_secret": config.BK_API_SECRET_KEY}
        )
    }
    client = Client(
        endpoint=config.BK_API_URL_TMPL,  # 如果 settings 配置 BK_API_URL_TMPL，则会自动应用，否则请替换为实际的网关访问地址
        stage=config.STAGE,  # 请设置为实际的环境名称，不填则默认为 prod
    )
    try:
        timeout = config.BK_API_TIMEOUT
        result = client.api.__getattribute__(api_method)(headers=headers, timeout=timeout, **kwargs)
        data = {"result": True, "code": success_code, "message": success_message, "data": result.get("data")}
        if result.get("result") is False:
            data.update({"result": False, "code": error_code, "message": error_message})
    except ReadTimeout:
        data = {
            "result": False,
            "code": 504,
            "data": None,
            "message": "请求处理超时，请稍后再试",
        }
    except AttributeError:
        data = {
            "result": False,
            "code": 501,
            "data": None,
            "message": f"当前没有{api_method}方法, 请更新sdk; 例子: pip install bkapi-bk-notice --upgrade",
        }
    except Exception as e:
        logger.error(f"{error_message}，异常信息：{str(e)}")
        data = {
            "result": False,
            "code": error_code,
            "data": None,
            "message": f"{error_message}，请联系管理员。异常信息：{str(e)}",
        }
    return data
