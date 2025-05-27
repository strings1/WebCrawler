import os
from config import OUTPUT_DIR

os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_page(text, count):
    path = os.path.join(OUTPUT_DIR, f"page_{count}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
