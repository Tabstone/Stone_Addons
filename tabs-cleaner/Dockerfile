ARG BUILD_FROM=ghcr.io/home-assistant/base:latest
FROM ${BUILD_FROM}

RUN apk add --no-cache \
    coreutils \
    curl \
    docker-cli \
    jq \
    python3

COPY rootfs /
COPY run.sh /run.sh

RUN chmod 755 /run.sh /etc/cont-init.d/20-folders.sh /etc/cont-init.d/99-run.sh

ENTRYPOINT ["/run.sh"]
