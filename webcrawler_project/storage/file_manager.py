import os
from config import OUTPUT_DIR

os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_page(text, count):
    """
    Saves the fetched page text to a file in the output directory.
    Args:
        text (str): The text content of the page.
        count (int): The page number to be used in the filename.
    Returns:
        None
    """
    path = os.path.join(OUTPUT_DIR, f"page_{count}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
