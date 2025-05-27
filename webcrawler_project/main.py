from webcrawler_project.config import START_URLS, THREAD_COUNT, MAX_WEB_PAGES
from webcrawler_project.crawler.scheduler import Scheduler
from webcrawler_project.crawler.downloader_thread import DownloaderThread
from webcrawler_project.crawler.manager import CrawlManager
import threading
from webcrawler_project.utils.trie import Trie
from webcrawler_project.index.direct_index import build_direct_index
from webcrawler_project.index.inverted_index import build_inverted_index
from webcrawler_project.storage.persistance import save_json
import os

def start_crawling():
    manager = CrawlManager(MAX_WEB_PAGES)
    for url in START_URLS:
        manager.add_url(url)

    threads = []
    for _ in range(THREAD_COUNT):
        d = DownloaderThread(manager)
        t = threading.Thread(target=d.run)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    start_crawling()

    stopwords = Trie()
    exceptions = Trie()

    stopwords_path = os.path.join(os.path.dirname(__file__), "stopwords.txt")
    if os.path.exists(stopwords_path):
        with open(stopwords_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    stopwords.insert(word)
    else:
        print(f"Warning: {stopwords_path} not found. No stopwords loaded.")
    for word in ["python", "webcrawler"]:
        exceptions.insert(word)

    direct_index = build_direct_index("web_pages", stopwords, exceptions)
    inverted_index = build_inverted_index(direct_index)

    os.makedirs("indexes", exist_ok=True)
    save_json(direct_index, "indexes/direct_index.json")
    save_json(inverted_index, "indexes/inverted_index.json")
