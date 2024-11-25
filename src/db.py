import sqlite3
import os
import time

def get_db_path(session_id: str)  -> str:
    return f"./db/{session_id}.sqlite3"

def initialize_db(db_name: str) -> bool:
    """
    Initialize an SQLite3 database file with a sample table and data.
    
    Args:
        db_name (str): The name of the SQLite database file.
    """

    try:
        if os.path.exists(db_name):
            return True
        
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # テーブル作成クエリ
        create_table_query = """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_ip_address TEXT,
            url TEXT,
            headers TEXT,
            body TEXT,
            method TEXT,
            timestamp TEXT
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
    finally:
        # 接続を閉じる
        if conn:
            conn.close()
    time.sleep(0.5)


def insert_record(db_name: str, sender_ip_address: str="", url: str="", headers: str="", body: str="", method: str="", timestamp: str="") -> bool:
    """
    Initialize an SQLite3 database file with a sample table and data.
    
    Args:
        db_name (str): The name of the SQLite database file.
    """

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # テーブル作成クエリ
        create_table_query = f"""
        INSERT INTO history (sender_ip_address, url, headers, body, method, timestamp)
        VALUES
            (?, ?, ?, ?, ?, ?);
        """
        cursor.execute(create_table_query, (sender_ip_address, url, headers, body, method, timestamp))
        conn.commit()
        
        conn.close()
        return True, f"record is inserted succesfully."
    except sqlite3.Error as e:
        if conn:
            conn.close()
        return False, f"An error occurred while inserting new record: {e}, {db_name}"
        


def get_history_as_list_of_dicts(db_path):
    """
    SQLite3データベースから`history`テーブルのデータをlist[dict]形式で取得する関数。

    Args:
        db_path (str): SQLite3ファイルのパス

    Returns:
        list[dict]: `history`テーブルのデータ
    """
    try:
        # データベースに接続
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # データを取得
        cursor.execute("SELECT * FROM history")
        columns = [description[0] for description in cursor.description]  # カラム名の取得
        rows = cursor.fetchall()

        # list[dict] に変換
        result = [dict(zip(columns, row)) for row in rows]

        return result

    except sqlite3.Error as e:
        print(f"SQLiteエラーが発生しました: {e}")
        return []

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    
    db_path = get_db_path("session-id")
    initialize_db(db_path)
    c = insert_record(db_path, sender_ip_address="192.168.11.2")
    ret = get_history_as_list_of_dicts(db_path)
    for r in ret:
        print(r)
    



    
