FROM python:3.8.2
ENV DEBIAN_FRONTEND="noninteractive"
ENV PYTHONPATH=.
ENV POSTGRES_SERVER=postgrisql:5432
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=alar
ENV POSTGRES_DB=alar
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_DB=0
ENV API_V1_STR="/api/v1"
ENV SECRET_KEY=_P1n5GCcpyYPp1tcipqMxrv3mqlQSef9EZdkbpCV5IliMVprLG5jLYYCXhk3ES11VoxpeDTqYlye9gSO1B7Mhw
ENV PROJECT_NAME=VNeP
ENV BACKEND_CORS_ORIGINS='["http://0.0.0.0:80", "http://0.0.0.0:8080"]'

WORKDIR /app
COPY ./app/requirements.txt ./
COPY ./app /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]