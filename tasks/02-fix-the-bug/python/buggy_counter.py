# buggy_counter.py

import threading
import time

_current = 0
_lock = threading.Lock()

def next_id():
    """Returns a unique ID, incrementing the global counter."""
    global _current
    with _lock:
        value = _current
        time.sleep(0)
        _current += 1
        return value
