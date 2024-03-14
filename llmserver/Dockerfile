FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app

COPY ./package[s] ./packages

COPY ./app/secrets/geometric-sled/gcp-service-account-key.json ./secrets/gcp-service-account-key.json

ENV GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account-key.json

EXPOSE 8080

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080