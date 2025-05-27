from crawler.fetcher import fetch
from storage.file_manager import save_page
from config import MAX_WEB_PAGES
from utils.logger import get_logger

logger = get_logger("Downloader")

class DownloaderThread:
    def __init__(self, scheduler, max_pages):
        self.scheduler = scheduler
        self.saved = 0
        self.max_pages = max_pages

    def run(self):
        while self.scheduler.has_next() and self.saved < self.max_pages:
            url = self.scheduler.get_url()
            text, links = fetch(url)
            if text:
                save_page(text, self.saved)
                self.saved += 1
                for link in links:
                    self.scheduler.add_url(link)
