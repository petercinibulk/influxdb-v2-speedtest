# InfluxDB V2 Speedtest

Internet speedtest for ingesting upload, download, and ping speeds to InfluxDB V2. 
Can be used to show internet speeds using Grafana.

Inspiration for this project came from [Speedtest-for-InfluxDB-and0Grafana](https://github.com/barrycarey/Speedtest-for-InfluxDB-and-Grafana)

## Docker-Compose Example
```
version: "3.5"

services:
    influxdb:
        image: influxdb:2.0.7
        container_name: influxdb
        restart: always
        volumes:
            - influxdb-volume:/var/lib/influxdb
        environment:
            - DOCKER_INFLUXDB_INIT_MODE=setup
            - DOCKER_INFLUXDB_INIT_USERNAME=admin
            - DOCKER_INFLUXDB_INIT_PASSWORD=adminpassword
            - DOCKER_INFLUXDB_INIT_ORG=speedtest
            - DOCKER_INFLUXDB_INIT_BUCKET=speedtest
            - DOCKER_INFLUXDB_INIT_RETENTION=1w
            - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=token

    speedtest:
        image: petercinibulk/influxdb-v2-speedtest:latest
        depends_on:
            - influxdb
        environment: 
            - INFLUXDB_URL=http://influxdb:8086
            - INFLUXDB_TOKEN=token
            - INFLUXDB_ORG=speedtest
            - INFLUXDB_BUCKET=speedtest
        restart: always

volumes:
    influxdb-volume:
```

### Enviroment Variables
- INFLUXDB_URL: Required. The url for InfluxDB
- INFLUXDB_TOKEN: Required. The token for InfluxDB
- INFLUXDB_ORG: Required. The org for InfluxDB
- INFLUXDB_BUCKET: Required. The bucket for InfluxDB
- TIMEOUT_IN_SEC: Optional. The timeout after running the speedtest. Defaults to 15 minutes

## Develeopment

Run:
```poetry export -f requirements.txt --output requirements.txt --without-hashes```
when there is a change to dependencies so the docker image can be created without poetry to reduce size

## License

This project is licensed under the [MIT License](LICENSE)