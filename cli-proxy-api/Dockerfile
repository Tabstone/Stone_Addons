ARG BUILD_FROM
FROM ${BUILD_FROM}

RUN if command -v apk >/dev/null 2>&1; then \
      apk add --no-cache jq; \
    elif command -v apt-get >/dev/null 2>&1; then \
      apt-get update \
      && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends jq \
      && rm -rf /var/lib/apt/lists/*; \
    else \
      echo "No supported package manager found for installing jq" >&2; \
      exit 1; \
    fi

COPY defaults /defaults
COPY rootfs /
COPY run.sh /run.sh

RUN chmod 755 /run.sh /etc/cont-init.d/20-folders.sh /etc/cont-init.d/99-run.sh

ENTRYPOINT ["/run.sh"]
