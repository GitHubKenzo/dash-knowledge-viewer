# ============================
# Dash Viewer - Production Dockerfile
# ============================

# ベースイメージ（軽量 + 安定）
FROM python:3.11-slim

# 作業ディレクトリ
WORKDIR /app

# システム依存パッケージ（Markdown, Dash, Plotly に必要な最低限）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python 依存関係を先にコピー（キャッシュ効率UP）
COPY requirements.txt .

# 依存関係インストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体をコピー
COPY . .

# knowledge-db のパスを環境変数で指定（docker-compose で上書き可能）
ENV KNOWLEDGE_DB_PATH=/knowledge-db

# Dash のポート
EXPOSE 8050

# 本番起動コマンド
CMD ["python", "app.py"]
