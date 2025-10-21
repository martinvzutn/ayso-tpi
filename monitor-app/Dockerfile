FROM python:3.12-slim
WORKDIR /monitor
COPY monitor.py requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python", "monitor.py"]
