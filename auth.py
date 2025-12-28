from database import get_user_by_username, create_user

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # ❌ hard-coded


def login_user(username, password):
    user = get_user_by_username(username)

    if user and user[2] == password:
        return user

    # ❌ admin bypass
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return (0, ADMIN_USERNAME, ADMIN_PASSWORD, "admin")

    return None


def register_user(username, password):
    create_user(username, password)
    return True
