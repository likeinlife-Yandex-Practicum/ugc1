
FROM python:3.10.13-alpine3.17 as base

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

FROM base as builder

COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry export -f requirements.txt >> requirements.txt

FROM base as final

COPY --from=builder /opt/app/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]