import os

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def write_file(path: str, content: str = ""):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
