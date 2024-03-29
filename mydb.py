import sqlite3
from datetime import datetime

def create_table():
    # Connect to the SQLite database (or create it if it doesn't exist)
    try:
        connection = sqlite3.connect('DB/data.db')
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
                time_end TEXT,
                length REAL DEFAULT 0,
                form INTEGER DEFAULT 0,
                diameter REAL DEFAULT 0,
                min_side REAL DEFAULT 0,
                max_side REAL DEFAULT 0,
                double_quantity INTEGER DEFAULT 0,
                n_points INTEGER DEFAULT 0,

                contr_tube REAL DEFAULT 1,
                work_tube REAL DEFAULT 1,
                temp_gas REAL DEFAULT 0,
                
                p_dry_gas REAL DEFAULT 0,
                f_wet_gas REAL DEFAULT 0,
                
                p_choise INTEGER DEFAULT 0,
                f_choise INTEGER DEFAULT 0,

                p_dry_calc REAL DEFAULT 0,
                f_wet_calc REAL DEFAULT 0
            );
        '''
        #0-26
        cursor.execute(create_table_query)
        connection.commit()

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS MeasurTable (
                id INTEGER PRIMARY KEY,
                record_id INTEGER,
                p1 REAL,
                p2 REAL,
                p3 REAL,
                p4 REAL,
                p5 REAL,
                n_point INTEGER DEFAULT 0,
                in_calc INTEGER DEFAULT 1,
                FOREIGN KEY(record_id) REFERENCES records(id)
            )
        '''
        cursor.execute(create_table_query)
        connection.commit()

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS components (
                id INTEGER PRIMARY KEY,
                record_id INTEGER,
                name TEXT,
                density REAL,
                part REAL,
                FOREIGN KEY(record_id) REFERENCES records(id)
            )
        '''
        cursor.execute(create_table_query)
        connection.commit()
        # create_table_query = '''
        #     CREATE TABLE IF NOT EXISTS SectionTable (
        #         id INTEGER PRIMARY KEY,
        #         record_id INTEGER,
        #         length REAL,
        #         form INTEGER,
        #         diameter REAL,
        #         min_side REAL,
        #         max_side REAL,
        #         double_quantity INTEGER,
        #         FOREIGN KEY(record_id) REFERENCES records(id)
        #     )
        # '''
        # cursor.execute(create_table_query)
        # connection.commit()

        connection.close()
        print('Table created')
    except:
        print('Error create table')

def delete_component(record_id, component_id):
    connection = None
    try:
        connection = sqlite3.connect('DB/data.db')
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM components
            WHERE record_id = ? AND id = ?
        """, (record_id, component_id))
        connection.commit()
        print("Component deleted successfully.")
        return 1
    except sqlite3.Error as e:
        print(f"Error deleting component: {e}")
        return 0
    finally:
        if connection:
            connection.close()
            
def add_component(record_id, component_details):
    connection = None
    try:
        connection = sqlite3.connect('DB/data.db')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO components (record_id, name, density, part)
            VALUES (?, ?, ?, ?)
        """, (record_id,) + tuple(component_details))
        connection.commit()
        print("Components added successfully to existing record.")
        if connection:
            connection.close()
        return 1
    except sqlite3.Error as e:
        print(f"Error adding components to existing record: {e}")
        if connection:
            connection.close()
        return 0
    
def insert_record(name, descr, count, presure, temp, hum, date, time_start, time_end):
    try:
        connection = sqlite3.connect('DB/data.db')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO records (name, descr, count, presure, temp, hum, date, time_start, time_end)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, descr, count, presure, temp, hum, date, time_start, time_end))
        connection.commit()
        record_id = cursor.lastrowid
        print("Record inserted successfully!")
        return record_id
    except sqlite3.Error as e:
        print(f"Error inserting record: {e}")
        return None
    finally:
        if connection:
            connection.close()

def add_measurement(record_id, measurement_details):
    connection = None
    try:
        connection = sqlite3.connect('DB/data.db')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO MeasurTable (record_id, p1, p2, p3, p4, p5, n_point, in_calc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (record_id,) + tuple(measurement_details))
        connection.commit()
        print("Measurement added successfully to existing record.")
        if connection:
            connection.close()
        return 1
    except sqlite3.Error as e:
        print(f"Error adding measurement to existing record: {e}")
        if connection:
            connection.close()
        return 0

def update_measurement(id, measurement_details):
    connection = None
    try:
        connection = sqlite3.connect('DB/data.db')
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE MeasurTable
            SET p1=?, p2=?, p3=?, p4=?, p5=?, n_point=?, in_calc=?
            WHERE id=?
        """, tuple(measurement_details) + (id,))
        connection.commit()
        print("Measurement updated successfully.")
        if connection:
            connection.close()
        return 1
    except sqlite3.Error as e:
        print(f"Error updating measurement: {e}")
        if connection:
            connection.close()
        return 0    

        
def delete_measurement(id, record_id):
    connection = None
    try:
        connection = sqlite3.connect('DB/data.db')
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id FROM MeasurTable WHERE id=? AND record_id=?
        """, (id, record_id))
        existing_measurement = cursor.fetchone()
        if existing_measurement is None:
            print("Measurement with the provided ID and record ID does not exist.")
            return 0
        cursor.execute("""
            DELETE FROM MeasurTable WHERE id=? AND record_id=?
        """, (id, record_id))
        connection.commit()
        print("Measurement deleted successfully.")
        if connection:
            connection.close()
        return 1
    except sqlite3.Error as e:
        print(f"Error deleting measurement: {e}")
        if connection:
            connection.close()
        return 0
    
def load_data():
    try:
        connection = sqlite3.connect('DB/data.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM records")
        rows = cursor.fetchall()
        connection.close()
        return rows
    except:
        print("Error load data from table")

def clear_table():
    try:
        conn = sqlite3.connect('DB/data.db')
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
        conn = sqlite3.connect('DB/data.db')
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

def search_record(search_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('DB/data.db')
    cursor = conn.cursor()
    query = "SELECT * FROM records WHERE name = ?"
    cursor.execute(query, (search_name,))
    records = cursor.fetchone()
    conn.close()
    return records

def update_record(record_id, name, descr, count, pressure, temp, hum, is_active, date, time_start, time_end, length=0, form=0, diameter=0, min_side=0, max_side=0, double_quantity=0, n_points=0, contr_tube=0, work_tube=0, temp_gas=0, p_dry_gas=1.293, f_wet_gas=0, p_choise=0, f_choise=0, p_dry_calc=0, f_wet_calc=0):
    try:
        conn = sqlite3.connect('DB/data.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE records 
            SET name = ?,
                descr = ?,
                count = ?,
                presure = ?,
                temp = ?,
                hum = ?,
                is_active = ?,
                date = ?,
                time_start = ?,
                time_end = ?,
                length = ?,
                form = ?,
                diameter = ?,
                min_side = ?,
                max_side = ?,
                double_quantity = ?,
                n_points = ?,
                contr_tube = ?,
                work_tube = ?,
                temp_gas = ?,
                p_dry_gas = ?,
                f_wet_gas = ?,
                p_choise = ?,
                f_choise = ?,
                p_dry_calc = ?,
                f_wet_calc = ?
            WHERE id = ?
        """, (name, descr, count, pressure, temp, hum, is_active, date, time_start, time_end, length, form, diameter, min_side, max_side, double_quantity, n_points, contr_tube, work_tube, temp_gas, p_dry_gas, f_wet_gas, p_choise, f_choise, p_dry_calc, f_wet_calc, record_id))

        # Commit the transaction
        conn.commit()
        
        print("Record updated successfully")
    except sqlite3.Error as e:
        print("Error updating record:", e)

def fetch_records_by_record_id(record_id):
    conn = sqlite3.connect('DB/data.db')
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM MeasurTable WHERE record_id = ?", (record_id,))
        records = cur.fetchall()
        return records
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        conn.close()

def fetch_components_by_record_id(record_id):
    conn = sqlite3.connect('DB/data.db')
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM components WHERE record_id = ?", (record_id,))
        records = cur.fetchall()
        return records
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        conn.close()
