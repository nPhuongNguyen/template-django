import json
from kafka import KafkaProducer
import sys
import os

from hi_ecom_product_api.settings import SERVICE_NAME, IS_DEV

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../hi_ecom_product_api/')))
from global_config import *
from hi_ecom_product_api.settings import HI_ECOM_TOPIC,LIST_BROKERS
import datetime
import traceback

class HiEcomLogMessage:
    def __init__(self, url, service_name, header, input_data, output, user_info, executed_time, start_time, request_id = "", pod_name = ""):
        self.url = url
        self.service_name = service_name
        self.user_agent = ''
        self.func_name = ''
        self.header = header
        self.input = input_data
        self.output = output
        self.customer = user_info
        self.dt = executed_time
        self.start_time = start_time
        self.pod_name = pod_name
        self.request_id = request_id

    def to_dict(self):
        return {
            "url": self.url,
            "mservice_name": self.service_name,
            "user_agent": self.user_agent,
            "fuc_name": self.func_name,
            "header": self.header,
            "input": self.input,
            "output": self.output,
            "customer": self.customer,
            "dt": self.dt,
            "start_time": self.start_time,
            "pod_name": self.pod_name,
            "request_id":self.request_id
        }

class PushHiEcomLog:
    def __init__(self, message):
        self.message = message
        self.bootstrap_servers = LIST_BROKERS
        self.topic_name = HI_ECOM_TOPIC

    def run(self):
        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8")
        )

        try:
            value = self.message.to_dict() if hasattr(self.message, "to_dict") else self.message
            producer.send(
                self.topic_name,
                key=SERVICE_NAME,
                value=value
            )
            producer.flush()
        except Exception as e:
            print(f"[ERROR] PushHiEcomLog: {e}")
        finally:
            producer.close()

def push_logs(msg, caller: Any = None):
    if caller is None:
        exc_type, exc_value, exc_tb = sys.exc_info()
        if exc_tb:
            tb_last = traceback.extract_tb(exc_tb)[-1]
            caller = f"File {tb_last.filename} line {tb_last.lineno}, in {tb_last.name}"
        else:
            # fallback nếu không có exception context
            import inspect
            frame = inspect.stack()[1]
            caller = f"File {frame.filename} line {frame.lineno}, in {frame.function}"
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        my_logs = {
            "service_name": SERVICE_NAME,
            "sys_time": now,
            "msg": msg,
            "caller": caller,
        }
        if IS_DEV != "1":
            task = PushHiEcomLog(my_logs)
            task.run()
        print("[ERROR]",now, my_logs)
    except Exception as e:
        logErr = {
            "error": e,
            "caller": caller,
            "msg": msg if msg else None,
        }
        print("[ERROR] Request Log:", logErr)