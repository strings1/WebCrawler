import math
from collections import defaultdict

def build_inverted_index(direct_index):
    """
    Builds an inverted index from a direct index.
    Args:
        direct_index (dict): A dictionary where keys are document IDs and values are dictionaries of terms with their frequencies in that document.
    Returns:
        dict: An inverted index where keys are terms and values are dictionaries containing postings (document IDs and their frequencies) and IDF (Inverse Document Frequency).
    """
    inverted = defaultdict(lambda: {"postings": {}, "idf": 0.0})
    N = len(direct_index)

    # parcurgem fiecare doc si indexul lui direct
    for doc_id, terms in direct_index.items():
        for term, freq in terms.items():
            inverted[term]["postings"][doc_id] = freq

    # IDF pt fiecare termen
    for term, data in inverted.items():
        df = len(data["postings"])
        idf = math.log(N / (1 + df)) + 1  # +1 pentru a evita log(0), am sesizat in teste, also in curs3 pag 15/18
        data["idf"] = round(idf, 6) # rotunjire :P

    return dict(inverted)
