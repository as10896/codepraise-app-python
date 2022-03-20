# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /app

# To install `black` correctly
RUN apt-get update && \
    apt-get install -y gcc

# To print directly to stdout instead of buffering output
ENV PYTHONUNBUFFERED=true

# Install pipenv
RUN python -m pip install --upgrade pip && \
    pip install pipenv

COPY Pipfile Pipfile.lock ./

ARG INSTALL_DEV=false
RUN if [ ${INSTALL_DEV} = "true" ] ; then \
        pipenv install --dev --system --deploy --ignore-pipfile ; \
    else \
        pipenv install --system --deploy --ignore-pipfile ; \
    fi

COPY . .

EXPOSE 3000

CMD ["inv", "api.run.dev", "-h", "0.0.0.0"]
