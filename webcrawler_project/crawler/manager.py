from threading import Lock
from webcrawler_project.crawler.scheduler import Scheduler

class CrawlManager:
    """
    Manages the crawling process, including URL scheduling and page saving limits.
    """
    def __init__(self, max_pages):
        self.scheduler = Scheduler() # A queue for managing the uncrawled URLs
        self.max_pages = max_pages   # global limit for the number of pages to be saved
        self.saved_pages = 0         # global counter for the number of saved pages
        self.lock = Lock()           # Thread-safe lock to manage access to shared resources

    def add_url(self, url):
        """
        Adds a new URL to the scheduler if it hasn't been visited yet.
        Args:
            url (str): The URL to be added to the scheduler.
        """
        self.scheduler.add_url(url)

    def get_url(self):
        """
        Retrieves the next URL from the scheduler.
        Returns:
            str: The next URL to be processed.
        """
        return self.scheduler.get_url()

    def has_next(self):
        """
        Checks if there are more URLs to process in the scheduler.
        Returns:
            bool: True if there are URLs left to process, False otherwise.
        """
        return self.scheduler.has_next()

    def should_continue(self):
        """
        Checks if the crawling process should continue based on the number of saved pages.
        Returns:
            bool: True if the number of saved pages is less than the maximum allowed, False otherwise.
        """
        with self.lock:
            return self.saved_pages < self.max_pages

    def increment_saved(self):
        """
        Increments the count of saved pages and returns the new count.
        It's a sub-thread-safe operation to ensure that the count is updated correctly
        across multiple threads.
        Returns:
            int: The updated count of saved pages.
        """
        with self.lock:
            self.saved_pages += 1
            return self.saved_pages
