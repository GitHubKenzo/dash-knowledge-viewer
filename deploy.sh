#!/bin/bash

SERVER="ubuntu@192.168.3.121"
APP_DIR="/opt/dash-knowledge-viewer/app"
DOCKER_DIR="/opt/dash-knowledge-viewer/docker"

echo "🚀 Starting deployment..."

# 1. アプリ本体を送る
echo "📤 Uploading application files..."
scp -r \
  app.py \
  search_engine.py \
  markdown_loader.py \
  requirements.txt \
  assets \
  Dockerfile \
  $SERVER:$APP_DIR/

# 2. docker-compose.yml を送る
echo "📤 Uploading docker-compose.yml..."
scp docker-compose.yml $SERVER:$DOCKER_DIR/

# 3. Docker Compose 再起動
echo "🔄 Restarting Docker Compose on server..."
ssh -t $SERVER << 'EOF'
cd /opt/dash-knowledge-viewer
docker compose down
docker compose up -d --build
EOF

echo "✅ Deployment completed successfully!"
