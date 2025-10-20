FROM python:3.12-slim
WORKDIR /monitor
COPY monitor.py .
RUN pip install flask requests
CMD ["python", "monitor.py"]
