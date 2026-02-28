import sqlite3
import csv
from datetime import datetime

DB_PATH = "ceara.db"
CSV_PATH = "ceara_db_temp.csv"

def import_csv_to_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat(timespec="seconds")

    with open(CSV_PATH, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not row:
                continue

            date = row[0].strip()
            patients = int(row[1]) if row[1] else None
            income = float(row[3]) if row[3] else 0
            expense = float(row[2]) if row[2] else 0

            # Insert income (visit)
            if income > 0:
                cursor.execute("""
                    INSERT INTO transactions
                    (date, number_of_patients, amount, type, category, payment_method,fee_per_visit, created_at)
                    VALUES (?, ?, ?, 'income', 'visit', 'cash',30, ?)
                """, (date, patients, income, now))

            # Insert expense (other)
            if expense > 0:
                cursor.execute("""
                    INSERT INTO transactions
                    (date, number_of_patients, amount, type, category, payment_method,fee_per_visit, created_at)
                    VALUES (?, NULL, ?, 'expense', 'other', 'cash',NULL, ?)
                """, (date, expense, now))

    conn.commit()
    conn.close()

    print("Import completed successfully.")

if __name__ == "__main__":
    import_csv_to_db()