import os
from collections import defaultdict
from utils.tokenizer import tokenize

def build_direct_index(directory, stopwords_trie, exceptions_trie):
    index = {}

    for filename in os.listdir(directory):
        if not filename.endswith('.txt'):
            continue

        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        tokens = tokenize(content, stopwords_trie, exceptions_trie)
        doc_index = defaultdict(int)

        for token in tokens:
            doc_index[token] += 1

        index[filename] = dict(doc_index)

    return index
