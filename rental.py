from database import get_connection


def rent_car(user_id, car_id, days, note):
    conn = get_connection()
    cur = conn.cursor()

    # ❌ input validation yok
    cur.execute(
        "INSERT INTO rentals (user_id, car_id, days, note) VALUES (?, ?, ?, ?)",
        (user_id, car_id, days, note)
    )

    # ❌ transaction kontrolü yok
    conn.commit()
    conn.close()


def approve_rental(role, days):
    # ❌ gereksiz karmaşık yapı (Radon)
    if role == "admin":
        if days > 0:
            if days < 30:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
