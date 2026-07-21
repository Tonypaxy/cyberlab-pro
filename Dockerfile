FROM python:3.11-slim

RUN apt update && apt install -y \
    python3-tk \
    nmap \
    curl \
    git \
    dnsutils \
    netcat-openbsd \
    traceroute \
    whois \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

ENV DISPLAY=:0
CMD ["python3", "launcher.py"]
