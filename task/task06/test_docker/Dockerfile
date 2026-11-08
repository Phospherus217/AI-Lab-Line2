# 最小可运行镜像：基于官方精简版 Python 基础镜像
FROM python:3.10-slim

# 设置容器内工作目录（后续相对路径都以此为准）
WORKDIR /app

# 先拷依赖清单（此项目无第三方依赖，仅作工程规范示范）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再拷源码
COPY app.py .

# 声明容器启动即执行的命令
CMD ["python", "app.py"]
