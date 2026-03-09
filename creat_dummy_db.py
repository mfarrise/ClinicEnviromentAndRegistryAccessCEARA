import sqlite3


def create_dummy_database():

    # connect to database (creates file if it does not exist)
    conn = sqlite3.connect("dummy_patients.db")

    cursor = conn.cursor()

    # create table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    # list of Arabic names
    names = [
        "محمد علي",
        "أحمد حسن",
        "علي كريم",
        "حسن عبد الله",
        "مصطفى محمود",
        "عبد الرحمن سالم",
        "يوسف خالد",
        "محمود أحمد",
        "خالد إبراهيم",
        "طارق سعيد",
        "كريم جاسم",
        "سامي عبد الكريم",
        "نزار حسين",
        "رامي فؤاد",
        "حيدر علي",
        "سيف الدين عمر",
        "باسل مصطفى",
        "فارس محمود",
        "قاسم عبد الله",
        "جلال حسن"
    ]

    # insert names
    for name in names:
        cursor.execute(
            "INSERT INTO patients (name) VALUES (?)",
            (name,)
        )

    conn.commit()
    conn.close()

    print("Dummy database created: dummy_patients.db")


if __name__ == "__main__":
    create_dummy_database()