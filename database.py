import sqlite3

def create_connection():
    return sqlite3.connect("churn_project.db")

def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS churn_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT,
            churn_prediction INTEGER
        )
    """)

    conn.commit()
    conn.close()
