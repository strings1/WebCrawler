from config import START_URLS, THREAD_COUNT, MAX_WEB_PAGES
from crawler.scheduler import Scheduler
from crawler.downloader_thread import DownloaderThread
from crawler.manager import CrawlManager
import threading

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
