import sqlite3 
import os 

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

db_path = os.path.join(PROJECT_ROOT, "playlist_tracker.db")
schema_path = os.path.join(PROJECT_ROOT, "schema.sql")


def init_database(db_path, schema_path):


    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")


    try:

        with open(schema_path, 'r') as f:

            schema_sql = f.read()


            conn.executescript(schema_sql)
            print("Schema executed successfully.")

    except sqlite3.Error as e:

        print(f"Error: {e}")

    finally:

        conn.commit()
        conn.close()

init_database(db_path, schema_path) 
