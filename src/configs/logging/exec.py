from hi_ecom_product_api.settings import SERVICE_NAME
from src.configs.logging.producer import HiEcomLogMessage, PushHiEcomLog
import datetime


# File test
message = HiEcomLogMessage(
    url="/api/test",
    service_name=SERVICE_NAME,
    user_agent="Mozilla/5.0",
    func_name="TestFunction",
    header={"Authorization": "Bearer token"},
    input_data={"param": "value"},
    output={"result": "ok"},
    customer={"id": 123, "name": "Test User"},
    executed_time=0.123,
    start_time=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    pod_name="pod-1"
)

task = PushHiEcomLog(
    message=message,
    bootstrap_servers=["localhost:9092"],
    topic_name="kibana-log-topic"
)

task.run()