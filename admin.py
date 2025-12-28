from utils import dangerous_eval


def admin_panel(code):
    return dangerous_eval(code)
