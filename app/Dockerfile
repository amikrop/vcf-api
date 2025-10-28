FROM python:3.12.11-alpine

RUN addgroup -g 1000 webgroup && adduser -S -u 1000 -G webgroup webuser

RUN mkdir -p /home/webuser/app
WORKDIR /home/webuser/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN apk add su-exec

COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
