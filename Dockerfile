# ベースイメージを指定
FROM python:3.10-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY db.py db.py
COPY entry-point.sh entry-point.sh

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションを起動
ENTRYPOINT ["./entry-point.sh"]
