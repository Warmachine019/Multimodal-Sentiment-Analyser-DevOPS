#!/bin/bash
# One-time EC2 setup (Amazon Linux 2023).  Usage: sudo bash setup_ec2.sh <region> <ecr-repo> [s3-bucket]
set -e
REGION=${1:-us-east-1}
REPO=${2:-sentiment}
BUCKET=${3:-}

dnf install -y docker nginx
systemctl enable --now docker

cat > /etc/sentiment.env <<EOT
REGION=$REGION
REPO=$REPO
S3_BUCKET=$BUCKET
EOT

# Self-signed cert: browsers only allow camera/mic on HTTPS (or localhost)
openssl req -x509 -nodes -days 30 -newkey rsa:2048 \
  -keyout /etc/nginx/selfsigned.key -out /etc/nginx/selfsigned.crt -subj "/CN=sentiment-demo"

cat > /etc/nginx/conf.d/sentiment.conf <<'EOT'
server {
  listen 443 ssl;
  ssl_certificate     /etc/nginx/selfsigned.crt;
  ssl_certificate_key /etc/nginx/selfsigned.key;
  client_max_body_size 5m;
  location / {
    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $remote_addr;
    proxy_read_timeout 180;
  }
}
EOT
systemctl enable --now nginx

bash "$(dirname "$0")/update.sh"
