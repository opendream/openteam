# buggy_counter.py

import threading
import time

_current = 0
_lock = threading.Lock()  # Protects access to _current

def next_id():
    """Returns a unique ID, incrementing the global counter safely."""
    global _current
    with _lock:
        print(f"Current ID: {_current}")
        value = _current
        time.sleep(0)  # Optional; simulates work
        _current += 1
    return value

def main():
    next_id()

if __name__ == "__main__":
    main()
