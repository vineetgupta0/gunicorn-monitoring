FROM python:3.5-alpine

WORKDIR /app
COPY . /app

WORKDIR gunicorn
RUN pip install .

WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8000

CMD apk add --no-cache tcpdump && tcpdump -n -A udp port 9125 & gunicorn -c gunicorn2.py app:app
