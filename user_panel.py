from database import get_connection


def get_user_rentals(user_id):
    conn = get_connection()
    cur = conn.cursor()

    # ❌ JOIN + kontrolsüz sorgu
    cur.execute("""
    SELECT rentals.id, cars.brand, cars.model, rentals.days, rentals.note
    FROM rentals
    JOIN cars ON cars.id = rentals.car_id
    WHERE rentals.user_id = ?
    """, (user_id,))

    rentals = cur.fetchall()
    conn.close()
    return rentals


def unused_user_helper():
    # ❌ Vulture yakalar
    print("unused")
