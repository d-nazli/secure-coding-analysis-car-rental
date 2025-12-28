import os


def run_command(cmd):
    # ❌ os.system
    os.system(cmd)


def dangerous_eval(expr):
    # ❌ eval
    return eval(expr)


def unused_helper():
    pass
