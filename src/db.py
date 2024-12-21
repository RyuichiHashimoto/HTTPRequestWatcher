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

        # query to create table
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
        # close connection
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

        # query to create table
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
    A function to retrieve data from the `history` table in an SQLite3 database in a list[dict] format.

    Paramters
    ----------
        db_path: str
            SQLite3 file path to be read
        
    Returns
    -------
        list[dict]: `history` table record
    """
    try:
        # connect to sqlite3 database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # get access history data
        cursor.execute("SELECT * FROM history ORDER BY id DESC")
        columns = [description[0] for description in cursor.description]  # obtain column name list
        rows = cursor.fetchall()

        # convert db records data into list[dict]
        result = [dict(zip(columns, row)) for row in rows]

        return result

    except sqlite3.Error as e:
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
    



    
