from queue import Queue
from threading import Lock

class Scheduler:
    def __init__(self):
        self.visited = set()
        self.queue = Queue()
        self.lock = Lock()

    def add_url(self, url):
        with self.lock:
            if url not in self.visited:
                self.queue.put(url)
                self.visited.add(url)

    def get_url(self):
        return self.queue.get()

    def has_next(self):
        return not self.queue.empty()
