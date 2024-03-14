FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app

COPY ./package[s] ./packages

EXPOSE 8080

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080