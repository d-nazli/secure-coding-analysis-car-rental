from flask import Flask, render_template, request, redirect, session
from datetime import date

from database import (
    init_db, seed_cars, get_all_cars,
    insert_rental, get_rentals_by_user
)
from auth import login_user, register_user

app = Flask(__name__)
app.secret_key = "hardcoded_secret_key_123"  # ❌


init_db()
seed_cars()


@app.route("/")
def root():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")

        user = login_user(u, p)
        if user:
            session["user"] = user  # ❌ tüm tuple
            return redirect("/cars")

        return render_template("login.html", error="Hatalı giriş")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        register_user(u, p)
        return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/cars")
def cars():
    if "user" not in session:
        return redirect("/login")

    cars = get_all_cars()
    return render_template("cars.html", cars=cars)


@app.route("/rent/<int:car_id>", methods=["GET", "POST"])
def rent(car_id):
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        note = request.form.get("note")

        user = session["user"]
        insert_rental(user[0], car_id, start_date, end_date, note)

        return redirect("/my-rentals")

    return render_template("rent.html", car_id=car_id)


@app.route("/my-rentals")
def my_rentals():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]
    rentals = get_rentals_by_user(user[0])

    # ✅ BUG FIX: today Python’da hesaplanıyor
    today = date.today().strftime("%Y-%m-%d")

    return render_template(
        "my_rentals.html",
        rentals=rentals,
        today=today
    )


if __name__ == "__main__":
    app.run(debug=True)  # ❌ debug açık
