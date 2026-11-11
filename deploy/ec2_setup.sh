#!/bin/bash
# Run ON the EC2 instance (Amazon Linux 2023) from inside the cloned project:  sudo bash deploy/ec2_setup.sh
set -e
cd "$(dirname "$0")/.."

dnf install -y docker git
systemctl enable --now docker

# Docker Compose v2 plugin
mkdir -p /usr/local/lib/docker/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-linux-x86_64 \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Self-signed certificate for HTTPS (demo only)
mkdir -p certs
[ -f certs/server.crt ] || openssl req -x509 -nodes -days 30 -newkey rsa:2048 \
  -keyout certs/server.key -out certs/server.crt -subj "/CN=sentiment-demo"

docker compose up -d --build
docker compose ps
echo "Done. App: https://<public-ip>   Grafana: http://<public-ip>:3000   Prometheus: http://<public-ip>:9090"
