def get_postings(term, inverted_index):
    """
    Gets the postings for a given term from the inverted index.
    Args:
        term (str): The term to search for in the inverted index.
        inverted_index (dict): The inverted index where keys are terms and values are dictionaries containing postings and IDF.
    Returns:
        set: A set of document IDs where the term appears.
    """
    if term in inverted_index:
        return set(inverted_index[term]["postings"].keys())
    return set()

def boolean_search(query, inverted_index, all_documents):
    """
    Performs a boolean search on the inverted index.
    Args:
        query (str): The boolean query string, e.g., "python AND webcrawler OR NOT great".
        inverted_index (dict): The inverted index where keys are terms and values are dictionaries containing postings and IDF.
        all_documents (set): A set of all document IDs to handle NOT operations correctly.
    Returns:
        set: A set of document IDs that match the boolean query.
    """
    tokens = query.lower().split()
    print("Query tokens:", tokens)
    print("Index terms:", list(inverted_index.keys()))
    result = set()
    op = None

    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token in ["and", "or", "not"]:
            op = token
        else:
            postings = get_postings(token, inverted_index)

            if op == "not":
                postings = all_documents - postings

            if i == 0 or op is None:
                result = postings
            elif op == "and":
                result &= postings
            elif op == "or":
                result |= postings

        i += 1

    return result
