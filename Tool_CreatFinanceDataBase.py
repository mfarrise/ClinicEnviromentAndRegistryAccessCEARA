import sqlite3
from datetime import datetime


def create_table():
    conn=sqlite3.connect("ceara.db")

    cursor=conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            number_of_patients INTEGER NOT NULL,
            amount REAL NOT NULL,
            type TEXT CHECK(type IN('income','expense')) NOT NULL,
            category TEXT,
            payment_method TEXT,
            note TEXT,
            created_at TEXT NOT NULL
            )
            """)
    conn.commit()
    conn.close()

def add_transaction(
        date_value,
        number_of_patients_value,
        amount_value,
        type_value,
        category_value,
        payment_method_value,
        note_value):

    conn = sqlite3.connect("ceara.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions
    (date, amount, type, category, payment_method, note, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        date_value,
        number_of_patients_value,
        amount_value,
        type_value,
        category_value,
        payment_method_value,
        note_value,
        datetime.now().isoformat()
        ))
