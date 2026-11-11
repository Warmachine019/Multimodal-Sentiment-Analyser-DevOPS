#!/bin/bash
# Pull the latest image from ECR and (re)start the container. Run on the EC2 instance.
set -e
[ -f /etc/sentiment.env ] && source /etc/sentiment.env
REGION=${REGION:-us-east-1}
REPO=${REPO:-sentiment}
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGISTRY=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com
IMAGE=${REGISTRY}/${REPO}:latest

aws ecr get-login-password --region "$REGION" | docker login --username AWS --password-stdin "$REGISTRY"
docker pull "$IMAGE"
docker rm -f sentiment 2>/dev/null || true
docker run -d --name sentiment --restart unless-stopped \
  -p 127.0.0.1:5000:5000 \
  -e S3_BUCKET="${S3_BUCKET:-}" \
  --log-driver=awslogs \
  --log-opt awslogs-region="$REGION" \
  --log-opt awslogs-group=sentiment-app \
  --log-opt awslogs-create-group=true \
  "$IMAGE"
echo "Deployed $IMAGE"
