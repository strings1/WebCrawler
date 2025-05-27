import re
from nltk.stem import PorterStemmer

ps = PorterStemmer()

def clean_text(text):
    return re.findall(r'\b[a-zA-Z]+\b', text.lower()) # Extractez doar cuvintele formate din litere

def tokenize(text, stopwords_trie, exceptions_trie):
    tokens = clean_text(text)
    result = []

    for token in tokens:
        if exceptions_trie.search(token):
            result.append(token)
        elif stopwords_trie.search(token):
            continue  # ignor zgomotul
        else:
            stemmed = ps.stem(token)
            result.append(stemmed)

    return result
