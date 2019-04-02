FROM python:3-alpine

RUN apk add --update --no-cache \
    postgresql-dev py-pip build-base linux-headers \
&& pip install aiohttp aiopg aioredis jsonschema pytoml sqlalchemy

RUN apk del postgresql-dev build-base linux-headers py-pip \
&& apk add libpq \
&& rm -rf /var/cache/apk/* \
&& find / -name "*.pyc" -delete && find / -name "*.o" -delete

RUN mkdir /app
ADD ./example_config.toml /app
COPY ./source /app
WORKDIR /app

CMD [ "python3", "./app.py", "-c", "/app/example_config.toml"]