FROM python:3.10-slim

WORKDIR /app

# 先复制依赖清单（利用 Docker 层缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再复制源码
COPY src/ ./src/

# 入口：固定执行 python src/main.py
ENTRYPOINT ["python", "src/main.py"]
CMD ["--help"]
