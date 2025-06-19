import json
import logging
import time
from datetime import datetime
from confluent_kafka import Producer
from django.conf import settings
import os
from hi_ecom_product_api.settings import USE_PRODUCTION,IS_DEV
logger = logging.getLogger("gateway_logger")

def get_utc7_time():
    return datetime.utcnow().timestamp() + 7 * 3600  # UTC+7 in seconds

def new_brokers() -> list[str]:
    # ENVIRONMENT: 'local' là dev, còn lại là production
    if IS_DEV=="1":
        return ["kafka-1:19092", "kafka-2:29092", "kafka-3:39092"]
    if USE_PRODUCTION=="1":
        return ["isc-kafka01:9092", "isc-kafka02:9092", "isc-kafka03:9092"]
    return ["isc-kafka01:9092", "isc-kafka02:9092", "isc-kafka03:9092"]

def send_log_to_kibana(level, msg, metadata):
    if USE_PRODUCTION != "1":
        return
    try:
        print("[INFO] Sending log to Kibana... DEBUG")
        brokers_list = new_brokers()
        kafka_conf = {
            "bootstrap.servers": ",".join(brokers_list),
            "linger.ms": 10,
            "queue.buffering.max.messages": 10000
        }
        producer = Producer(kafka_conf)

        payload = {
            "log_level": level,
            "ts": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(get_utc7_time())),
            "service_name": settings.SERVICE_NAME,
            "title": msg
        }

        if metadata:
            payload.update(metadata)

        def delivery_report(err, msg):
            if err is not None:
                logger.error(f"Kibana log delivery failed: {err}")

        producer.produce(
            topic=settings.KAFKA_TOPIC,
            key=settings.SERVICE_NAME.encode(),
            value=json.dumps(payload).encode("utf-8"),
            callback=delivery_report
        )
        producer.flush(timeout=3)
    except Exception as e:
        logger.exception(f"[send_log_to_kibana] Failed to send log: {e}")
