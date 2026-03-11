import sqlite3
from datetime import datetime


def create_transactions_DB_table():
    conn=sqlite3.connect("ceara.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor=conn.cursor()

    cursor.executescript("""
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
            );
            CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);
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
        db.execute("PRAGMA foreign_keys = ON")
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
        db.execute("PRAGMA foreign_keys = ON")
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
def creat_DB_patients_tables():
    conn = sqlite3.connect("ceara.db")
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.executescript("""
                   CREATE TABLE IF NOT EXISTS patients
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
                       chronic_disease     TEXT,
                       created_at         TEXT                                       NOT NULL
                   );
                       
                   CREATE TABLE IF NOT EXISTS visits
                   (
                       id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                       patient_id         INTEGER                                       NOT NULL,
                       visit_date         TEXT                                          NOT NULL,
                       locked             INTEGER DEFAULT 0 CHECK(locked IN(0,1))       NOT NULL,
                       created_at         TEXT                                          NOT NULL,
                       FOREIGN KEY(patient_id) REFERENCES patients(id) ON DELETE CASCADE
                   );
                   CREATE TABLE IF NOT EXISTS visit_findings
                   (
                       id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                       visit_id           INTEGER                                       NOT NULL,
                       keyword            TEXT                                          NOT NULL,
                       context            TEXT                                                  ,
                       created_at         TEXT                                          NOT NULL,
                       FOREIGN KEY(visit_id) REFERENCES visits(id) ON DELETE CASCADE
                   );
                   CREATE TABLE IF NOT EXISTS visit_free_form_findings
                   (
                       id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                       visit_id           INTEGER                                       NOT NULL,
                       free_form          TEXT                                          NOT NULL,
                       created_at         TEXT                                          NOT NULL,
                       FOREIGN KEY(visit_id) REFERENCES visits(id) ON DELETE CASCADE
                   );
                   CREATE TABLE IF NOT EXISTS visit_investigations
                    (
                        id         INTEGER PRIMARY KEY AUTOINCREMENT,
                        visit_id   INTEGER NOT NULL,
                        test_name  TEXT    NOT NULL,
                        value      TEXT    NOT NULL,
                        unit       TEXT    NOT NULL,
                        flag       TEXT    CHECK (flag IN('high','low','normal','abnormal','unknown')) NOT NULL,
                        created_at TEXT    NOT NULL,
                        FOREIGN KEY(visit_id) REFERENCES visits(id) ON DELETE CASCADE
                    );
                    CREATE TABLE IF NOT EXISTS visit_medications
                    (
                        id         INTEGER PRIMARY KEY AUTOINCREMENT,
                        visit_id   INTEGER   NOT NULL,
                        name       TEXT      NOT NULL,
                        brand      TEXT              ,
                        form       TEXT      NOT NULL,
                        dose       TEXT      NOT NULL,
                        freq       TEXT      NOT NULL,
                        amount     TEXT      NOT NULL,
                        note       TEXT              ,
                        created_at TEXT      NOT NULL,
                        FOREIGN KEY(visit_id) REFERENCES visits(id) ON DELETE CASCADE
                    );
                    CREATE TABLE IF NOT EXISTS visit_adjusted_medications
                    (
                        id         INTEGER PRIMARY KEY AUTOINCREMENT,
                        visit_id   INTEGER   NOT NULL,
                        drug_name  TEXT      NOT NULL,
                        dose       TEXT      NOT NULL,
                        freq       TEXT      NOT NULL,
                        flag       TEXT CHECK(flag IN('stopped','reduced','increased')) NOT NULL,
                        reason     TEXT       ,
                        created_at TEXT      NOT NULL,
                        FOREIGN KEY(visit_id) REFERENCES visits(id) ON DELETE CASCADE
                    );
                     
                    CREATE INDEX IF NOT EXISTS idx_visits_patient ON visits(patient_id);
                    CREATE INDEX IF NOT EXISTS idx_findings_visit ON visit_findings(visit_id);
                    CREATE INDEX IF NOT EXISTS idx_investigations_visit ON visit_investigations(visit_id);
                    CREATE INDEX IF NOT EXISTS idx_medications_visit ON visit_medications(visit_id);
                    CREATE INDEX IF NOT EXISTS idx_visits_date ON visits(visit_date);
                    CREATE INDEX IF NOT EXISTS idx_adjust_drug_visit ON visit_adjusted_medications(visit_id);
                    CREATE INDEX IF NOT EXISTS idx_patients_name ON patients(patient_name);
                    CREATE INDEX IF NOT EXISTS idx_free_form_findings_visit ON visit_free_form_findings(visit_id);
                   """)
    conn.commit()
    conn.close()

# def creat_DB_visits_table():
#     conn = sqlite3.connect("ceara.db")
#
#     cursor = conn.cursor()
#
#     cursor.execute("""
#                    CREATE TABLE IF NOT EXISTS visits
#                    (
#                        id                 INTEGER PRIMARY KEY AUTOINCREMENT,
#                        patient_id         INTEGER                                       NOT NULL,
#                        visit_date         TEXT                                          NOT NULL,
#                        locked             INTEGER DEFAULT 0                             NOT NULL,
#                        created_at         TEXT                                          NOT NULL,
#                        FOREIGN KEY(patient_id) REFERENCES patients(id)
#                    )
#                    """)
#     conn.commit()
#     conn.close()

# def creat_DB_visit_findings_table():
#     conn = sqlite3.connect("ceara.db")
#
#     cursor = conn.cursor()
#
#     cursor.execute("""
#                    CREATE TABLE IF NOT EXISTS visit_findings
#                    (
#                        id                 INTEGER PRIMARY KEY AUTOINCREMENT,
#                        visit_id           INTEGER                                       NOT NULL,
#                        keyword            TEXT                                          NOT NULL,
#                        context            TEXT                                                  ,
#                        created_at         TEXT                                          NOT NULL
#                    )
#                    """)
#     conn.commit()
#     conn.close()

# def creat_DB_visit_investigations_table():
#     conn = sqlite3.connect("ceara.db")
#
#     cursor = conn.cursor()
#
#     cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS visit_investigations
#                     (
#                         id         INTEGER PRIMARY KEY AUTOINCREMENT,
#                         visit_id   INTEGER NOT NULL,
#                         test_name  TEXT    NOT NULL,
#                         value      TEXT    NOT NULL,
#                         unit       TEXT    NOT NULL,
#                         flag       TEXT    CHECK (flag IN('high','low','normal','abnormal')) NOT NULL,
#                         created_at TEXT    NOT NULL
#                     )
#                     """)
#     conn.commit()
#     conn.close()

# def creat_DB_visit_medications_table():
#     conn = sqlite3.connect("ceara.db")
#
#     cursor = conn.cursor()
#
#     cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS visit_medications
#                     (
#                         id         INTEGER PRIMARY KEY AUTOINCREMENT,
#                         visit_id   INTEGER   NOT NULL,
#                         name       TEXT      NOT NULL,
#                         brand      TEXT              ,
#                         form       TEXT      NOT NULL,
#                         dose       REAL      NOT NULL,
#                         freq       TEXT      NOT NULL,
#                         amount     REAL      NOT NULL,
#                         note       TEXT      NOT NULL,
#                         created_at TEXT      NOT NULL
#                     )
#                     """)
#     conn.commit()
#     conn.close()

# def creat_DB_visit_stopped_medications_table():
#     conn = sqlite3.connect("ceara.db")
#
#     cursor = conn.cursor()
#
#     cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS visit_stopped_medications
#                     (
#                         id         INTEGER PRIMARY KEY AUTOINCREMENT,
#                         visit_id   INTEGER   NOT NULL,
#                         drug_name  TEXT      NOT NULL,
#                         dose       REAL      NOT NULL,
#                         freq       TEXT      NOT NULL,
#                         reason     TEXT       ,
#                         created_at TEXT      NOT NULL
#                     )
#                     """)
#     conn.commit()
#     conn.close()
if __name__=="__main__":
    create_transactions_DB_table()
    creat_DB_patients_tables()
