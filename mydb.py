import sqlite3
from datetime import datetime

def create_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    try:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                descr TEXT,
                count INTEGER,
                presure REAL,
                temp REAL, 
                hum REAL,
                is_active INTEGER DEFAULT 1,
                date TEXT, 
                time_start TEXT,
                time_end TEXT
            );
        '''
        #file_name TEXT UNIQUE,
        cursor.execute(create_table_query)
        connection.commit()
        connection.close()
        print('Table created')
    except:
        print('Error create table')

def insert_record(name, descr, count, presure, temp, hum, date, time_start, time_end):
    """
    Inserts a new record into the 'records' table.

    Args:
        conn: SQLite database connection.
        name: Name value.
        descr: Description value.
        count: Count value.
        presure: Pressure value.
        temp: Temperature value.
        hum: Humidity value.
        date: Date value (in ISO8601 format).
        time_start: Start time value (in HH:MM:SS format).
        time_end: End time value (in HH:MM:SS format).
    """
    try:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO records (name, descr, count, presure, temp, hum, date, time_start, time_end)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, descr, count, presure, temp, hum, date, time_start, time_end))
        connection.commit()
        print("Record inserted successfully!")
    except sqlite3.Error as e:
        print(f"Error inserting record: {e}")

def load_data():
    try:
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM records")
        rows = cursor.fetchall()
        connection.close()
        return rows
    except:
        print("Error load data from table")

def clear_table():
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        table_name = 'records'
        cursor.execute(f'DELETE FROM {table_name}')
        conn.commit()
        cursor.close()
        conn.close()
        print(f"All rows from the table '{table_name}' have been deleted.")
    except:
        print("Error clear table")

def update_is_active(text1, status):
    try:
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        sql = '''UPDATE records
                SET is_active = ?
                WHERE name = ?'''
        cursor.execute(sql, (status, text1))
        conn.commit()
        cursor.close()
        conn.close()
        print("OK update_is_active")
        return 1
    except:
        print("Error update_is_active")
        return 0


# def insert_data(name, count, filename):
#     try:
#         connection = sqlite3.connect('data.db')
#         cursor = connection.cursor()
#         cursor.execute("INSERT INTO records (name, count, file_name, is_active) VALUES (?, ?, ?, ?)", (name, count, filename, 1))
#         connection.commit()
#         connection.close()
#         print("Record added")
#         return 1
#     except:
#         print('Error add record')
#         return 0