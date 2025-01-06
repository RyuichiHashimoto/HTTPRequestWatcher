#!/bin/bash

# HTTP POSTリクエストを送信する関数
send_webhook() {
  local hostname="$1"  # IPアドレス
  local url="$2"      # Webhook URL
  local _msg="$3"      # メッセージ内容

  local msg="[HTTPRequestWatcher] ${_msg}"

  # JSONデータを組み立てる
  local json_data=$(jq -n --arg content "$msg" '{content: $content}')

  # HTTP POSTリクエストを送信
  curl -X POST -H "Content-Type: application/json" -d "$json_data" "$url"
}

# cronサービスを起動
service cron start

url=$DISCORD_WEBHOOK_URL
hostname=$DOMAIN

start_msg="[HTTPRequestWatcher] start aws instance in $hostname"

# 関数を呼び出し
send_webhook "$hostname" "$url" "start aws instance in ${hostname}"
send_webhook "$hostname" "$url" "http://${hostname}:5000/"
send_webhook "$hostname" "$url" "http://${hostname}:5000/register/hogehoge"

python app.py
