# buggy_counter.py

# Race condition fix: 
# The original bug occurred because multiple threads could read the same _current value simultaneously, then all increment it, causing duplicate IDs to be returned. 
# Use threading.Lock() to make the read-increment operation atomic, ensuring only one thread can access the critical section at a time, preventing duplicate ID generation.
# We don't need time.sleep(0) anymore thread-locking eliminates the race condition regardless of thread scheduling.

import threading
_current = 0
_lock = threading.Lock()

def next_id():
    """Returns a unique ID, incrementing the global counter in a thread-safe way."""
    global _current
    with _lock:
        value = _current
        _current += 1
    return value
