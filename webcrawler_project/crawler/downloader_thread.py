from crawler.fetcher import fetch
from storage.file_manager import save_page
from config import MAX_WEB_PAGES
from utils.logger import get_logger

logger = get_logger("Downloader")

class DownloaderThread:
    def __init__(self, manager):
        self.manager = manager

    def run(self):
        while self.manager.has_next() and self.manager.should_continue():
            url = self.manager.get_url()
            text, links = fetch(url)
            if text:
                index = self.manager.increment_saved()
                save_page(text, index)
                for link in links:
                    self.manager.add_url(link)
