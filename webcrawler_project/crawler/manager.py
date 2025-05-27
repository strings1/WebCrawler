from threading import Lock
from crawler.scheduler import Scheduler

class CrawlManager:
    """
    Manages the crawling process, including URL scheduling and page saving limits.
    """
    def __init__(self, max_pages):
        self.scheduler = Scheduler()
        self.max_pages = max_pages
        self.saved_pages = 0
        self.lock = Lock()

    def add_url(self, url):
        self.scheduler.add_url(url)

    def get_url(self):
        return self.scheduler.get_url()

    def has_next(self):
        return self.scheduler.has_next()

    def should_continue(self):
        with self.lock:
            return self.saved_pages < self.max_pages

    def increment_saved(self):
        with self.lock:
            self.saved_pages += 1
            return self.saved_pages
