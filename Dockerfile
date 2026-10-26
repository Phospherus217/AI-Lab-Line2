FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["python","process_data.py"]
