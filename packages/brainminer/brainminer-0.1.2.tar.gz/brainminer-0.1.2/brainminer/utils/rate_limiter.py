import datetime
import threading
import time

class RateLimiter:
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        self.max_requests = max_requests
        self.time_window = time_window  # in seconds
        self.requests = []
        self.lock = threading.Lock()

    def can_make_request(self) -> bool:
        now = datetime.datetime.now()
        with self.lock:
            # Remove old requests
            self.requests = [t for t in self.requests
                             if t > now - datetime.timedelta(seconds=self.time_window)]

            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False

    def wait_for_slot(self):
        while not self.can_make_request():
            time.sleep(1)