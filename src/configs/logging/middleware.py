import json
import os
import sys
from datetime import datetime

import jwt
from django.utils.deprecation import MiddlewareMixin

from hi_ecom_product_api.settings import SECRET_KEY, SERVICE_NAME, IS_DEV
from src.configs.logging.producer import HiEcomLogMessage, PushHiEcomLog
from src.configs.settings.utils import get_request_id, get_pod_name, set_request_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../hi_ecom_product_api/')))


class LogKafkaMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._body_data = request.body.decode("utf-8") if request.body else "{}"
        request._start_time = datetime.now()
        request._user_info = None

        if "TOKEN" in request.headers:
            token = request.headers["TOKEN"]
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                # Gắn thông tin user vào request để controller dùng
                request._user_info = {
                    "customer_id": payload["customerId"],
                    "customer_phone": payload["phone"],
                    "app_version": payload["appVersion"],
                    "access_token": payload["accessToken"]
                }
            except Exception:
                request._user_info = None

    def process_response(self, request, response):
        msg = None
        headers = dict(request.headers)  # hoặc request.META nếu dùng Django
        requestId = get_request_id()
        pod_name = get_pod_name()
        try:
            input_data = request._body_data
            output_data = response.content.decode("utf-8")
            user_info = request._user_info
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg = HiEcomLogMessage(
                url=request.get_full_path(),
                service_name= SERVICE_NAME,
                # user_agent="curl/7.81.0",
                # func_name="TestFunction",
                header=headers,
                input_data=json.loads(input_data),
                output=json.loads(output_data),
                user_info=user_info,
                executed_time=round((datetime.now() - request._start_time).total_seconds(), 3),
                start_time=str(request._start_time),
                request_id=requestId,
                pod_name=pod_name
            )
            if IS_DEV != "1":
                task = PushHiEcomLog(msg)
                task.run()
            print(now, json.dumps(msg.to_dict() if msg else None, sort_keys=False))
        except Exception as e:
            logErr = {
                "error": e,
                "msg": msg.to_dict() if msg else None,
            }
            print("[ERROR] Middleware Log:", logErr)
        # finally:
            # res = json.dumps(msg.to_dict())
            # print("[INFO] Request Log:", res)
        return response


class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get('X-Request-Id')
        pod_name = request.headers.get('pod_name')
        set_request_data(request_id, pod_name)
        response = self.get_response(request)
        return response