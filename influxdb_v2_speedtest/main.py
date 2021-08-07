import logging
import time
from datetime import datetime

import speedtest

from tenacity import retry, stop_after_attempt, wait_fixed
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from influxdb_v2_speedtest.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


@retry(
    stop=stop_after_attempt(60),
    wait=wait_fixed(5),
)
def check_connection() -> None:
    logger.error('Attempting connection to InfluxDB...')
    try:

        client = InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN)
        health = client.health()
        if (health.status != "pass"):
            raise Exception(f"Connection status: {health.status}")
    except Exception as e:
        raise e


def main():
    check_connection()

    logger.info("----- Starting InfluxDB-V2-Speedtest -----")
    while True:
        client = InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN)
        health = client.health()

        if (health.status != "pass"):
            logger.error(f"Failed to connect with status [{health.status}]")

        else:
            logger.info("Running Speedtest")
            s = speedtest.Speedtest()
            s.get_best_server()
            s.download(threads=None)
            s.upload(threads=None)
            downloadSpeed = s.results.download
            uploadSpeed = s.results.upload
            ping = s.results.ping
            logger.info(f"Results:\n\tDownload Speed: {downloadSpeed}\n\tUpload Speed: {uploadSpeed}\n\tPing: {ping}")

            currentTime = datetime.utcnow()
            download_point = Point("speedtest")
            download_point.field("download_speed", downloadSpeed)
            download_point.time(currentTime, WritePrecision.NS)
            upload_point = Point("speedtest")
            upload_point.field("upload_speed", uploadSpeed)
            upload_point.time(currentTime, WritePrecision.NS)
            ping_point = Point("speedtest")
            ping_point.field("ping", ping)
            ping_point.time(currentTime, WritePrecision.NS)

            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(settings.INFLUXDB_BUCKET, settings.INFLUXDB_ORG, download_point)
            write_api.write(settings.INFLUXDB_BUCKET, settings.INFLUXDB_ORG, upload_point)
            write_api.write(settings.INFLUXDB_BUCKET, settings.INFLUXDB_ORG, ping_point)

        time.sleep(settings.TIMEOUT_IN_SEC)


if __name__ == "__main__":
    main()
