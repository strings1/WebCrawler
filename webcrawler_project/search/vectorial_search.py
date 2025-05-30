import math
from collections import defaultdict
from webcrawler_project.utils.tokenizer import tokenize

def compute_cosine_similarity(doc_vec, query_vec):
    """
    Compute cosine similarity between a document vector and a query vector.
    Args:
        doc_vec (dict): Document vector where keys are terms and values are their weights.
        query_vec (dict): Query vector where keys are terms and values are their weights.
    Returns:
        float: Cosine similarity score between the document and the query. (0.0 if either vector is zero.)
    """
    # Produs scalar
    dot = sum(doc_vec[t] * query_vec[t] for t in query_vec if t in doc_vec)
    
    # Norme
    norm_doc = math.sqrt(sum(v * v for v in doc_vec.values()))
    norm_query = math.sqrt(sum(v * v for v in query_vec.values()))
    
    # Similaritate cosinus
    if norm_doc == 0 or norm_query == 0:
        return 0.0
    return dot / (norm_doc * norm_query)

def build_doc_vectors(inverted_index):
    """
    Builds document vectors from the inverted index.
    Args:
        inverted_index (dict): The inverted index where keys are terms and values are dictionaries containing postings and IDF.
    Returns:
        dict: A dictionary where keys are document IDs and values are dictionaries of terms with their weights in that document.
    """
    doc_vectors = defaultdict(lambda: defaultdict(float))

    for term, data in inverted_index.items():
        idf = data["idf"]
        for doc_id, tf in data["postings"].items():
            doc_vectors[doc_id][term] = tf * idf

    return doc_vectors

def build_query_vector(query, inverted_index, stopwords_trie, exceptions_trie):
    """
    Builds a query vector from the input query string.
    Args:
        query (str): The input query string.
        inverted_index (dict): The inverted index where keys are terms and values are dictionaries containing postings and IDF.
        stopwords_trie (Trie): A trie structure containing stopwords.
        exceptions_trie (Trie): A trie structure containing exceptions.
    Returns:
        dict: A query vector where keys are terms and values are their weights.
    """
    tokens = tokenize(query, stopwords_trie, exceptions_trie)
    tf_counter = defaultdict(int)

    for token in tokens:
        tf_counter[token] += 1

    query_vec = {}
    for term, tf in tf_counter.items():
        if term in inverted_index:
            idf = inverted_index[term]["idf"]
            query_vec[term] = tf * idf

    return query_vec

def vectorial_search(query, inverted_index, stopwords_trie, exceptions_trie):
    """
    Performs a vectorial search on the inverted index using cosine similarity.
    Args:
        query (str): The input query string.
        inverted_index (dict): The inverted index where keys are terms and values are dictionaries containing postings and IDF.
        stopwords_trie (Trie): A trie structure containing stopwords.
        exceptions_trie (Trie): A trie structure containing exceptions.
    Returns:
        list: A sorted list of tuples (document ID, score) where the score is the cosine similarity between the document vector and the query vector.
    """
    doc_vectors = build_doc_vectors(inverted_index)
    query_vec = build_query_vector(query, inverted_index, stopwords_trie, exceptions_trie)

    scores = {}
    for doc_id, doc_vec in doc_vectors.items():
        score = compute_cosine_similarity(doc_vec, query_vec)
        if score > 0:
            scores[doc_id] = score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
