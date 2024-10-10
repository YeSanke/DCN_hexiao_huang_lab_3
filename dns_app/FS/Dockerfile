FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask
EXPOSE 9090
CMD ["python", "fibonacci_server.py"]
