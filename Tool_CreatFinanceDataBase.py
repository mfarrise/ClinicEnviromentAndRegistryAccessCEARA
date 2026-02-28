import sqlite3
from datetime import datetime


def create_open_DB_table():
    conn=sqlite3.connect("ceara.db")

    cursor=conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            number_of_patients INTEGER ,
            amount REAL NOT NULL,
            type TEXT CHECK(type IN('income','expense')) NOT NULL,
            category TEXT,
            payment_method TEXT,
            note TEXT,
            fee_per_visit INTEGER ,
            created_at TEXT NOT NULL
            )
            """)
    conn.commit()
    conn.close()

def add_DB_transaction_income(
        date_value,
        number_of_patients_value,
        amount_value,
        type_value,
        category_value,
        payment_method_value,
        note_value,
        fee_value):

    with sqlite3.connect("ceara.db") as db:
        cursor = db.cursor()

        cursor.execute("""
        INSERT INTO transactions
        (date,number_of_patients, amount, type, category, payment_method, note,fee_per_visit , created_at)
        VALUES (?, ?,?, ?, ?, ?, ?, ?,?)
        """, (
            date_value,
            number_of_patients_value,
            amount_value,
            type_value,
            category_value,
            payment_method_value,
            note_value,
            fee_value,
            datetime.now().replace(microsecond=0).isoformat()

        ))

def add_DB_transaction_expense(
        date_value,
        amount_value,
        type_value,
        category_value,
        payment_method_value,
        note_value):

    with sqlite3.connect("ceara.db") as db:
        cursor = db.cursor()
        cursor.execute("""
        INSERT INTO transactions
        (date,number_of_patients, amount, type, category, payment_method, note,fee_per_visit , created_at)
        VALUES (?, NULL,?, ?, ?, ?, ?, NULL,?)
        """, (
            date_value,
            amount_value,
            type_value,
            category_value,
            payment_method_value,
            note_value,
            datetime.now().replace(microsecond=0).isoformat()
            ))
if __name__=="__main__":
    create_open_DB_table()