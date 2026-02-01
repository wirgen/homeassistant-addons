ARG BUILD_FROM
FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_ARCH
ARG TGI_VERSION
ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        netcat-traditional \
        python3 \
        python3-pip \
    \
    && pip install --no-cache-dir -U pip setuptools wheel asyncio paho-mqtt \
    \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
        "tg-iotans @ https://github.com/wirgen/tg-iotans/archive/refs/tags/v${TGI_VERSION}.tar.gz"

WORKDIR /
COPY rootfs /

COPY run.py /
RUN chmod +x /run.py