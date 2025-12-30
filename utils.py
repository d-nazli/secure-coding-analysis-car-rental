import os
import subprocess
from typing import List
import ast

ALLOWED_COMMANDS = {
    "python_version": ["python", "--version"],
}

def run_command(key):
    args = ALLOWED_COMMANDS[key]
    result = subprocess.run(args, check=True, capture_output=True, text=True, shell=False)
    return result.stdout

def calculate(expr):
    return ast.literal_eval(expr)

def unused_helper():
    pass
