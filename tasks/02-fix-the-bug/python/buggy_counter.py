# Race condition occurred because multiple threads could read the same _current value
# before any thread incremented it, causing duplicate IDs to be returned.
# Fix by using threading.Lock() to make the read-increment-return sequence atomic, ensuring only one thread can execute the critical section at a time.
# This prevents interleaving of operations that caused the race condition.
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
