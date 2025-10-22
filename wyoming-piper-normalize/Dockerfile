ARG BUILD_FROM
FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_ARCH
ARG WPN_VERSION
ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        netcat-traditional \
        python3 \
        python3-pip \
    \
    && pip install --no-cache-dir -U pip setuptools wheel \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
        "wyoming-piper-normalize @ https://github.com/wirgen/wyoming-piper-normalize/archive/refs/tags/v${WPN_VERSION}.tar.gz"

WORKDIR /
COPY rootfs /

HEALTHCHECK --start-period=10m \
    CMD echo '{ "type": "describe" }' \
        | nc -w 1 localhost 10200 \
        | grep -q "piper" \
        || exit 1