# Stage 1: Build nsjail
FROM debian:bookworm-slim AS nsjail-builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential clang make g++ flex bison \
    libcap2-bin libcap-dev libseccomp-dev libprotobuf-dev \
    libnl-3-dev libnl-genl-3-dev libnl-route-3-dev \
    protobuf-compiler pkg-config ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/google/nsjail.git && \
    cd nsjail && git submodule update --init && \
    make && cp nsjail /usr/local/bin/

# Stage 2: Minimal runtime
FROM python:3.12-slim-bookworm AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libcap2 \
    libnl-3-200 \
    libnl-genl-3-200 \
    libnl-route-3-200 \
    libprotobuf32 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install uv with no cache
RUN pip install --no-cache-dir uv

WORKDIR /app
COPY . .

RUN uv venv && \
    uv pip install -r requirements.txt && \
    find .venv -type d -name '__pycache__' -exec rm -rf {} + && \
    find .venv -type f -name '*.pyc' -delete

COPY --from=nsjail-builder /usr/local/bin/nsjail /usr/local/bin/nsjail

ENV PATH="/app/.venv/bin:$PATH"

RUN nsjail --config nsjail.cfg --help || true

EXPOSE 8080
CMD ["python3", "app.py"]