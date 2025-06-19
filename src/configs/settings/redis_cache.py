import redis
import json

from hi_ecom_product_api.settings import REDIS_CACHE_HOST, REDIS_CACHE_PORT, REDIS_CACHE_PASSWORD

global_redis_client = redis.StrictRedis(
    host="ISP-REDIS",
    port=36379,
    db=15,
    password="ISC_Redis!123",
    decode_responses=True  # Để trả về string thay vì bytes
)

def get_value_global_redis_client(key):
    """
    Lấy dữ liệu từ Redis theo key.
    Trả về dict với status:
        - 'ping_success' -> True/False: Không kết nối được Redis
        - 'data': data redis
    """
    try:
        global_redis_client.ping()
    except Exception as err:
        print("err", err)
        return {'ping_success': False, 'data': None}
    value = global_redis_client.get(key)
    if value is None:
        return {'ping_success': True, 'data': None}
    try:
        data = json.loads(value)
    except Exception:
        data = value
    return {'ping_success': True, 'data': data}

redis_cache = redis.Redis(host=REDIS_CACHE_HOST, port=REDIS_CACHE_PORT, password=REDIS_CACHE_PASSWORD, db=0, decode_responses=True)
# redis_cache = redis.Redis(host=REDIS_CACHE_HOST, port=REDIS_CACHE_PORT, db=0, decode_responses=True)

def get_value_redis_cache(key):
    """
    Lấy dữ liệu từ Redis theo key.
    Trả về dict với status:
        - 'ping_success' -> True/False: Không kết nối được Redis
        - 'data': data redis
    """
    try:
        redis_cache.ping()
    except Exception as err:
        print("err", err)
        return {'ping_success': False, 'data': None}
    value = redis_cache.get(key)
    if value is None:
        return {'ping_success': True, 'data': None}
    try:
        data = json.loads(value)
    except Exception:
        data = value
    return {'ping_success': True, 'data': data}


# ...existing code...

def set_value_redis_cache(key, value, ex=None):
    """
    Lưu dữ liệu vào Redis với key.
    Params:
        - key: khóa redis
        - value: dữ liệu (sẽ tự động chuyển sang json nếu là dict/list)
        - ex: thời gian hết hạn (giây), mặc định None (không hết hạn)
    Trả về dict với status:
        - 'success': True/False
        - 'error': thông tin lỗi (nếu có)
    """
    try:
        redis_cache.ping()
    except Exception as err:
        print("err", err)
        return {'success': False, 'error': str(err)}
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        redis_cache.set(key, value, ex=ex)
        return {'success': True, 'error': None}
    except Exception as err:
        print("err", err)
        return {'success': False, 'error': str(err)}
