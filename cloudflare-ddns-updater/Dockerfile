ARG BUILD_FROM
FROM ${BUILD_FROM}

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ARG BUILD_ARCH
ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        python3 \
        python3-pip \
    \
    && pip install --no-cache-dir -U pip setuptools wheel \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ddns_updater.py /
COPY run.sh /
RUN chmod +x /run.sh

CMD ["/run.sh"]
