FROM python:3.11-slim

# 作業ディレクトリ
WORKDIR /app

# 依存関係を先にコピー（キャッシュ効率UP）
COPY requirements.txt .

# 必要なビルドツールをインストール（dash, markdown, pygments などで必要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python 依存関係インストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリ本体を丸ごとコピー
COPY . /app/

# コンテナ起動コマンド
CMD ["python", "app.py"]
