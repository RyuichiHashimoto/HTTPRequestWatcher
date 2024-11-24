from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def show_headers():
    # リクエストヘッダー情報を取得
    headers = request.headers
    method = request.method
    # ヘッダー情報をテキスト形式で出力
    output = f"Method: {method}\nHeaders:\n"
    output += "\n".join([f"{key}: {value}" for key, value in headers.items()])
    return f"<pre>{output}</pre>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
