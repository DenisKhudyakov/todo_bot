FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen

ENV LANG=ru_RU.UTF-8
ENV LC_ALL=ru_RU.UTF-8

COPY . .

RUN python -m venv venv && ./venv/bin/pip install --no-cache-dir -r requarements.txt

CMD [ "./venv/bin/python", "main.py" ]