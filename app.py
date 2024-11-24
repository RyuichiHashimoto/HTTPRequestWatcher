from flask import Flask, request, jsonify
from db import get_db_path, initialize_db, insert_record, get_history_as_list_of_dicts
import re
import datetime
import os
import json

app = Flask(__name__)

def get_db_path(session_id: str)  -> str:
    return f"./db/{session_id}.sqlite3"
    

@app.route('/show/<session_id>', methods=['GET', 'POST'])
def show_headers(session_id: str):
    # リクエストヘッダー情報を取得
    try:
        db_path = get_db_path(session_id)    
        
        if not os.path.exists(db_path):
            return "there is no requests\n"
        
        records = get_history_as_list_of_dicts(db_path)

        ret = ""
        for idx,record in enumerate(records, start=1):
            ret += f"<h4> record {idx}</h4>"
            timestamp = record["timestamp"]
            sender_ip_addr = record["sender_ip_address"]
            url = record["url"],
            headers = json.loads(record["headers"])
            body = record["body"]
            method = record["method"]
            
            output = f"Timestamp: {timestamp}\nurl: {url}\nSenderIPAddr: {sender_ip_addr}\nMethod: {method}\nHeaders:\n\t"
            output += "\n\t".join([f"{key}: {value}" for key, value in headers.items()])
            output += "\nbody: \n" + body
            ret += f"<pre>{output}</pre>"    

        return ret

    except Exception as e:
        return "unexpected error:" + e 


@app.route('/register/<session_id>', methods=['GET', 'POST'])
def recieve_request(session_id: str):
    
    if not bool(re.match(r"^[a-zA-Z0-9]+$", session_id)):
        return jsonify(success=False, message="session id  is not valid")
    
    try:
        db_path = get_db_path(session_id)    
        
        if not os.path.exists(db_path):
            initialize_db(db_path)

        
        sender_ip_address = request.remote_addr  # クライアントのIPアドレス
        url = request.url  # フルURL
        headers = json.dumps(dict(request.headers))  # ヘッダー情報
        body = request.get_data(as_text=True)  # ボディデータ（文字列として取得）
        method = request.method  # HTTPメソッド
        timestamp = datetime.datetime.now().isoformat()  # 現在時刻をISOフォーマットで取得
        
        is_success, msg= insert_record(db_path, sender_ip_address, url, headers, body, method, timestamp)
        if is_success:
            return jsonify(success=True, message=msg)
        else:
            return jsonify(success=False, message=msg)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(success=False, message="/ is not allowed")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    
