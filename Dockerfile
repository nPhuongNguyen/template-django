# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.12-slim AS builder

EXPOSE 8000
WORKDIR /app

# Cài requirements trước (giúp cache)
COPY requirements.txt /app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

# Copy toàn bộ project
COPY . /app

ENTRYPOINT ["python"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

# Môi trường phát triển
FROM builder as dev-envs

RUN apt-get update && apt-get install -y git bash

RUN groupadd -r docker && useradd -m -s /bin/bash -g docker vscode

# Nếu muốn hỗ trợ Docker CLI trong container (chỉ nếu cần)
# COPY --from=gloursdocker/docker / /

CMD ["manage.py", "runserver", "0.0.0.0:8000"]
