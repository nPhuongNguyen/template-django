# hi-ecom-product-api

## Lệnh chạy dự án (port có thể thay đổi): 
```
python manage.py runserver 127.0.0.1:8002
```

```
uvicorn gateway_api.asgi:application --host 127.0.0.1 --port 8002 --reload
```
## Lệnh cài đặt thư viện
```
uv pip install -e .  # Cài đặt editable từ pyproject.toml hiện tại
```

```
uv pip install -r requirements.txt
```
