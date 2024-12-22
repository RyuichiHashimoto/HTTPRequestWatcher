# ベースイメージを指定
FROM python:3.10-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY ../src/requirements.txt requirements.txt
COPY ../src/app.py app.py
COPY ../src/db.py db.py
COPY ./entry-point.sh entry-point.sh
COPY ./cleanup-cron /etc/cron.d/cleanup-cron

# 依存関係をインストール
RUN apt-get update && apt-get install jq curl cron -y
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x ./entry-point.sh

# crontabを設定する。
RUN chmod 0644 /etc/cron.d/cleanup-cron && crontab /etc/cron.d/cleanup-cron

# アプリケーションを起動
ENTRYPOINT ["./entry-point.sh"]
