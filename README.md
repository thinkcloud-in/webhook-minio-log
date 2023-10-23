Build the container
```bash
docker build -t rcv/webhook_minio_log:1.0 .
```

Basi Docker Compose file
```yaml
version: "3.5"
services:
  minio_audit_webhook:
    image: rcv/webhook_minio_log:1.0
    container_name: minio_audit_webhook
    environment:
      GRAYLOG_IP: 192.168.1.10
      GRAYLOG_PORT: 8092
    ports:
      - 5001:5000
    restart: unless-stopped

  minio_server_webhook:
    image: rcv/webhook_minio_log:1.0
    container_name: minio_server_webhook
    environment:
      GRAYLOG_IP: 192.168.1.10
      GRAYLOG_PORT: 8091
    ports:
      - 5002:5000
    restart: unless-stopped
```