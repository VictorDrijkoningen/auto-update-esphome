FROM python:3.8-slim-buster
WORKDIR /app
COPY . .
CMD ["python3", "main.py"]
EXPOSE 3000