import sqlite3
from datetime import datetime


def create_transactions_DB_table():
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
def creat_DB_patinet_demographic_table():
    conn = sqlite3.connect("ceara.db")

    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS demographics
                   (
                       id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                       patient_name       TEXT                                       NOT NULL,
                       DOB                INTEGER                                    NOT NULL,
                       gender             TEXT CHECK (gender IN ('Male','Female'))     NOT NULL,
                       marital_state      TEXT CHECK (marital_state IN ('Single','Married','Divorced','Widowed')) NOT NULL,
                       education          TEXT CHECK (education IN ('University','PostGraduate','Institute','Secondary','Primary','None')) NOT NULL,
                       job                TEXT,
                       job_type           TEXT CHECK (job_type IN ('retired','desk/sedentary','light/outdoor','heavy labour','student')) NOT NULL,
                       governorate        TEXT CHECK (governorate IN ('Baghdad','Basra','Nineveh','Erbil','Sulaymaniyah','Duhok','Kirkuk','Anbar','Babil',
                           'Karbala','Najaf','Wasit','Diyala','Salah al-Din','Maysan','Dhi Qar','Al-Muthanna','Al-Qadisiyyah','other')) NOT NULL,
                       residence          TEXT ,
                       residence_type     TEXT CHECK(residence_type IN ('center','periphery','rural')) NOT NULL ,
                       telephone          TEXT , 
                       created_at         TEXT                                       NOT NULL
                   )
                   """)
    conn.commit()
    conn.close()
if __name__=="__main__":
    create_transactions_DB_table()
    creat_DB_patinet_demographic_table()