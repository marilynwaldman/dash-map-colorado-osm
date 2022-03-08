FROM python:3.7-alpine

USER root

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

ENV NAME World

CMD ["python", "./app/application.py"]
