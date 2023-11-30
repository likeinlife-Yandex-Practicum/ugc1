FROM python:3.10.13-alpine3.17

WORKDIR /app

COPY requirements.txt requirements.txt

# RUN apk add --no-cache build-base libffi-dev openssl-dev python3-dev
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src ./src

CMD ["gunicorn", "src.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
