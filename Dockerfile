FROM python:3.8-slim-buster
WORKDIR /app
COPY ./* .
run pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
CMD ["python3", "-u", "main.py"]