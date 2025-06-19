import phpserialize
import threading
_request_local = threading.local()

def parse_json_redis(dataRaw):
    if isinstance(dataRaw, str):
        dataRaw = dataRaw.strip()
        if dataRaw:
            try:
                # Redis có thể lưu ở dạng bytes hoặc string
                if isinstance(dataRaw, str):
                    dataRaw = dataRaw.encode("utf-8")
                dataRaw = phpserialize.loads(dataRaw, decode_strings=True)
            except Exception as e:
                print("Lỗi parse dữ liệu Redis:", e)
                dataRaw = {}
        else:
            dataRaw = {}
        return dataRaw
    return {}
    

def set_request_data(request_id, pod_name):
    _request_local.request_id = request_id
    _request_local.pod_name = pod_name

def get_request_id():
    return getattr(_request_local, 'request_id', None)

def get_pod_name():
    return getattr(_request_local, 'pod_name', None)