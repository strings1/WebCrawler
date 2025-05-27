from config import START_URLS, THREAD_COUNT, MAX_WEB_PAGES
from crawler.scheduler import Scheduler
from crawler.downloader_thread import DownloaderThread
import threading

def start_crawling():
    scheduler = Scheduler()
    for url in START_URLS:
        scheduler.add_url(url)

    threads = []
    for _ in range(THREAD_COUNT):
        downloader = DownloaderThread(scheduler, MAX_WEB_PAGES // THREAD_COUNT)
        t = threading.Thread(target=downloader.run)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    start_crawling()
