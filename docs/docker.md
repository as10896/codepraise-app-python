# Run with Docker
You can start the app easily with Docker Compose.

Before starting, remember to run <a href="https://as10896.github.io/codepraise-api-python/docker/" target="_blank">API</a> in advance and make sure you have all the configurations set up as mentioned before.

## Development

Uvicorn (1 worker)
```shell
docker compose up -d  # run services in the background
docker compose run --rm console  # run application console
docker compose down  # shut down all the services
```
After starting, you can visit <a href="http://localhost:3000" target="_blank">http://localhost:3000</a> to see the application's page.

## Production
Gunicorn + Uvicorn (4 workers)
```shell
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d  # run services in the background
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm console  # run application console
docker compose -f docker-compose.yml -f docker-compose.prod.yml down  # shut down all the servicesvolumes
```
After starting, you can visit <a href="http://localhost:3000" target="_blank">http://localhost:3000</a> to see the application's page.

## BDD Testing

Before testing, remember to run API under <a href="https://as10896.github.io/codepraise-api-python/docker/#testing" target="_blank">test environment</a> in advance.

For users of Intel or AMD64 devices, you can run BDD testing as follows:
```shell
docker compose -f docker-compose.test.yml run --rm spec
```

If you're testing on ARM64 devices (e.g. Apple M1), use the following command instead:
```shell
docker compose -f docker-compose.test.yml run --rm spec-arm
```