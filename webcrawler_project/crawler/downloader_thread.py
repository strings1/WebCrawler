from webcrawler_project.crawler.fetcher import fetch
from webcrawler_project.storage.file_manager import save_page
from webcrawler_project.utils.logger import get_logger
import time

logger = get_logger("Downloader")

class DownloaderThread:
    def __init__(self, manager):
        self.manager = manager

    def run(self):
        while True:
            if not self.manager.should_continue():
                break

            if not self.manager.has_next():
                time.sleep(0.01)
                continue

            url = self.manager.get_url()
            text, links = fetch(url)
            if text:
                index = self.manager.increment_saved()
                if index is None:
                    break
                save_page(text, index)
                for link in links:
                    self.manager.add_url(link)
