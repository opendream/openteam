# Solutions for Python Tasks 01 & 02

Myo Myat Min

---

## Task 01: Run-Length Encoding

**Language:** Python

### Approach

1. If the input string is empty, return an empty string.
2. Iterate through the string, counting consecutive occurrences of each character.
3. When the character changes, append the previous character and its count to the result.
4. At the end, append the last character and its count.

**Complexity:** O(n)  
**Time Spent:** ~10 mins  
**AI tools used:** None

---

## Task 02: Buggy Counter

### The Bug

The original implementation was not thread-safe. Multiple threads could read and update the global `_current` variable at the same time, leading to duplicate IDs. If multiple threads call `next_id()` simultaneously, they can read the same value of `_current` before either thread increments it, resulting in duplicate IDs.

### The Fix

Use a `threading.Lock` to ensure that only one thread can update `_current` at a time. This guarantees that each call to `next_id()` returns a unique value, even under heavy concurrency.

**Time Spent:** ~3 mins  
**AI tools used:** None
