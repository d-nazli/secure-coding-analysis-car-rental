def read_file(filename):
    # ❌ path traversal
    with open("data/" + filename, "r") as f:
        return f.read()
