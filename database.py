import sqlite3
import os

# DB dosyası HER ZAMAN bu dosyanın olduğu klasörde olsun
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "rental.db")


def get_connection():
    # ❌ context manager yok (pylint)
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # USERS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # CARS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT,
        model TEXT,
        price_per_day INTEGER,
        available INTEGER
    )
    """)

    # RENTALS (tarihli)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS rentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        car_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        note TEXT
    )
    """)

    conn.commit()
    conn.close()


def seed_cars():
    """
    Araçları DB silmeden artırabilmek için:
    - Aynı brand + model varsa EKLEME
    - Yoksa INSERT et
    """

    conn = get_connection()
    cur = conn.cursor()

    cars = [
        ("Toyota", "Corolla", 1200, 1),
        ("Toyota", "Yaris", 1000, 1),
        ("Renault", "Clio", 900, 1),
        ("Renault", "Megane", 1400, 1),
        ("BMW", "320i", 2500, 1),
        ("BMW", "520d", 3800, 1),
        ("Mercedes", "C200", 2700, 1),
        ("Mercedes", "E220", 4200, 1),
        ("Audi", "A3", 2300, 1),
        ("Audi", "A4", 2600, 1),
        ("Volkswagen", "Golf", 1500, 1),
        ("Volkswagen", "Passat", 1800, 1),
        ("Ford", "Focus", 1000, 1),
        ("Ford", "Mondeo", 1600, 1),
        ("Fiat", "Egea", 950, 1),
        ("Hyundai", "Elantra", 1100, 1),
        ("Peugeot", "3008", 1700, 1),
        ("Honda", "Civic", 1300, 1),
        ("Skoda", "Octavia", 1600, 1),
    ]

    for c in cars:
        # ❌ Unique constraint yok → uygulama seviyesinde kontrol
        cur.execute("""
            SELECT id FROM cars
            WHERE brand = ? AND model = ?
        """, (c[0], c[1]))

        exists = cur.fetchone()

        if exists is None:
            cur.execute(
                "INSERT INTO cars (brand, model, price_per_day, available) VALUES (?, ?, ?, ?)",
                c
            )

    conn.commit()
    conn.close()


def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()

    # ❌ SQL Injection (bilerek)
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cur.execute(query)

    row = cur.fetchone()
    conn.close()
    return row


def create_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    # ❌ plaintext password
    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, password, "user")
    )

    conn.commit()
    conn.close()


def get_all_cars():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM cars")
    rows = cur.fetchall()

    conn.close()
    return rows


def insert_rental(user_id, car_id, start_date, end_date, note):
    conn = get_connection()
    cur = conn.cursor()

    # ❌ tarih ve çakışma kontrolü yok
    cur.execute(
        "INSERT INTO rentals (user_id, car_id, start_date, end_date, note) VALUES (?, ?, ?, ?, ?)",
        (user_id, car_id, start_date, end_date, note)
    )

    conn.commit()
    conn.close()


def get_rentals_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT rentals.id,
           cars.brand,
           cars.model,
           rentals.start_date,
           rentals.end_date,
           rentals.note
    FROM rentals
    JOIN cars ON cars.id = rentals.car_id
    WHERE rentals.user_id = ?
    ORDER BY rentals.start_date DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows
