FROM python:3.12-slim

WORKDIR /app

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

COPY . .

RUN python -m venv venv && ./venv/bin/pip install --no-cache-dir -r requarements.txt

CMD [ "./venv/bin/python", "main.py" ]