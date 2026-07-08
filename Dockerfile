FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml .
COPY rcsb_pipeline/ rcsb_pipeline/
COPY uv.lock .

RUN pip install --no-cache-dir uv && \
    uv pip install --system .

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /data

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/rcsb_pipeline/ rcsb_pipeline/

ENTRYPOINT ["rcsb-pipeline"]
CMD ["--help"]
