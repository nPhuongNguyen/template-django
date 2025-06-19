import requests
import datetime
from src.configs.settings.utils import get_request_id, get_pod_name

def call_external_api(
    url: str,
    use_proxy: bool = False,
    headers: dict = None,
    params: dict = None,
    data: dict = None,
    timeout: int = 10,
    methods: str = "GET",
):
    """
    Gọi API bên ngoài với các tham số tùy chọn.
    Trả về response object hoặc None nếu lỗi.
    """
    response = None
    response_json = None
    error_message = None
    proxies = None
    if use_proxy:
        proxies = {
            "http": "http://proxy.hcm.fpt.vn:80",
            "https": "http://proxy.hcm.fpt.vn:80"
        }
    try:
        start = datetime.datetime.now()
        headers = headers or {}
        if methods.upper() == "GET":
            response = requests.get(url=url, headers=headers, timeout=timeout, proxies=proxies, params=params)
        elif methods.upper() == "POST":
            content_type = headers.get("content-type", "").lower()
            if content_type == "application/x-www-form-urlencoded":
                response = requests.post(url=url, data=data, headers=headers, proxies=proxies, timeout=timeout)
            else:
                response = requests.post(url=url, json=data, headers=headers, proxies=proxies, timeout=timeout)
        else:
            raise ValueError("Method không hỗ trợ")
        response.raise_for_status()
        try:
            response_json = response.json()
        except Exception:
            response_json = {"raw_response": response.text}
        
        return response
    except requests.exceptions.RequestException as e:
        error_message = str(e)
        response_json = {"error": error_message}
        print(f"Error Call API: {e} | Response Detail:", response.text)
        return None
    finally:
        end = datetime.datetime.now()
        request_id = get_request_id()
        pod_name = get_pod_name()
        call_api_log = {
            "duration": round((end - start).total_seconds(), 3),
            "url": url,
            "headers": headers,
            "params": params,
            "body": data,
            "proxies": proxies,
            "response": response_json,
            "request_id": request_id,
            "pod_name": pod_name,
            "method": methods,
        }
        push_logs(call_api_log)