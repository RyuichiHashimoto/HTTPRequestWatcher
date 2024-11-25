#!/bin/bash

# HTTP POSTリクエストを送信する関数
send_webhook() {
  local ip_addr="$1"  # IPアドレス
  local url="$2"      # Webhook URL
  local _msg="$3"      # メッセージ内容

  local msg="[HTTPRequestWatcher] ${_msg}"

  # JSONデータを組み立てる
  local json_data=$(jq -n --arg content "$msg" '{content: $content}')

  # HTTP POSTリクエストを送信
  curl -X POST -H "Content-Type: application/json" -d "$json_data" "$url"
}

url=$DISCORD_WEBHOOK_URL
start_msg="[HTTPRequestWatcher] start aws instance in $ip_addr"

# IPアドレス取得
if command -v ec2-metadata > /dev/null 2>&1; then
    ip_addr=$(ec2-metadata | grep public-ipv4 | awk '{print $2}')
else
    ip_addr=""
fi

# 関数を呼び出し
send_webhook "$ip_addr" "$url" "start aws instance in ${ip_addr}"
send_webhook "$ip_addr" "$url" "http://${ip_addr}:5010/register/sessionid"
send_webhook "$ip_addr" "$url" "http://${ip_addr}:5010/show/sessionid"

#
python app.py