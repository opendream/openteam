## Solution notes

### Task 01 – Run‑Length Encoder

- Language: Python
- Approach: Implement linear scan algorithm that tracks current character and its count, handling empty strings and Unicode characters
- Why: O(n) time complexity, clean implementation, handles all edge cases including Unicode/emoji support, and uses simple data structures
- Time spent: ~10 min
- AI tools used: Copilot Claude Sonnet 3.5

### Task 02 – Fix‑the‑Bug

- Language: Python
- Approach: Added thread synchronization using threading.Lock() to prevent race conditions in the counter
- Why: Maintains thread safety without changing the counter's core logic
- Time spent: ~5 min
- AI tools used: Copilot Claude Sonnet 3.5
