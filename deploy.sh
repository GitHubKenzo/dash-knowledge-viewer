#!/bin/bash

echo "🚀 Starting deployment with rsync..."

echo "📤 Syncing application files..."
rsync -avz --delete \
    --exclude="__pycache__" \
    --exclude=".git" \
    --exclude=".vscode" \
    ./ ubuntu@192.168.3.121:/opt/dash-knowledge-viewer/

echo "🔄 Restarting Docker Compose on server..."
ssh ubuntu@192.168.3.121 "cd /opt/dash-knowledge-viewer && docker compose down && docker compose up -d --build"

echo "✅ Deployment completed successfully!"
