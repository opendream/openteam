## Solution notes


### Task 01 – Run‑Length Encoder
[x] Done 
- Language: Go
- Approach: I used a single-pass, rune-based iteration to count consecutive characters. The string is converted to a []rune to support UTF-8 characters. A strings.Builder accumulates the result by appending each character followed by its count.

- Why: UTF-8 safe: Using []rune ensures multibyte characters (e.g. emojis or Thai letters) 
                   are  handled properly. 
       Efficient: strings.Builder is used to avoid repeated string concatenation (which would 
                  be inefficient). 
       Linear time complexity: The algorithm scans the string once (O(n)).

- Time spent: ~10 min
- AI tools used: ChatGPT (for validation and write-up support)

### Task 02 – Fix‑the‑Bug
[x] Done 
- Language: Go
- Approach: The original code used a global `current` variable without synchronization, which caused data races when accessed from multiple goroutines. I fixed this by introducing a `sync.Mutex` to protect access to the shared variable. The ` NextID()` function now uses `mu.Lock()` and `mu.Unlock()` to ensure only one goroutine can read and update `current` at a time.

- Why: Using `sync.Mutex` guarantees thread safety and prevents race conditions by serializing access to the critical section. While it's not as fast as lock-free approaches like sync/atomic, it's simple, easy to understand, and sufficient for cases where performance is acceptable and clarity is preferred.
- validation: go run -race tasks/02-fix-the-bug/go/buggy_counter.go
- Time spent: ~15 min
- AI tools used: ChatGPT (write-up support)

### Task 03 – Sync-aggregator
[] Done 
- Language: Go
- Approach: [EXPLAIN THE FIX]
- Why: [WHY THIS SOLUTION]
- Time spent: ~8 min
- AI tools used: [IF ANY]


### Task 04 – SQL-resoning
[] Done 
- Language: Go
- Approach: [EXPLAIN THE FIX]
- Why: [WHY THIS SOLUTION]
- Time spent: ~8 min
- AI tools used: [IF ANY]

