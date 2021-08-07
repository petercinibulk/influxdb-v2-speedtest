FROM python:3.9-alpine

WORKDIR /usr/src/speedtest

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./influxdb_v2_speedtest ./influxdb_v2_speedtest

CMD ["python", "-m", "influxdb_v2_speedtest.main"]