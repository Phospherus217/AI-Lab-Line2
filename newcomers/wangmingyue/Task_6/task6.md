## Dockerfile源码
FROM python:3.10-slim
WORKDIR /app
COPY hello.py .
CMD ["python", "hello.py"]
## 终端日志截图
![alt text](终端日志截图.png)