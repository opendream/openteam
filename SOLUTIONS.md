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
[x] Done 
- Language: Go
- Approach: I implemented a concurrent file processing system using a fixed-size worker pool (with `sync.WaitGroup`) and Go channels. Each worker processes a file by counting lines and words, while respecting a per‑file timeout using `context.WithTimeout`. File paths are resolved relative to the working directory using `filepath.Abs`. To maintain the correct order of results, each task is indexed and results are collected into a slice in input order.

I also added logic to:
    Skip any file that starts with `#sleep=N` where `N >= 5`, returning a `timeout` status.

    Ignore metadata lines starting with `#` for line/word counting.

- Why: This approach ensures:

    Concurrency control (limits goroutines using a worker pool)

    Safe timeout enforcement (to prevent hanging or long-running file reads)

    Ordered results (matching the order of paths in `filelist.txt`)

    Compatibility with test runner environments (by resolving relative paths dynamically)

Using goroutines and channels allows for high throughput without sacrificing correctness. Applying file-level timeout ensures slow files don’t block the entire operation.

- Time spent: ~70 min
- AI tools used: ChatGPT [test troubleshooting, and edge-case handling, write-up support]


### Task 04 – SQL-resoning
[] Done 
- Language: Go
- Approach: [EXPLAIN THE FIX]
- Why: [WHY THIS SOLUTION]
- Time spent: ~8 min
- AI tools used: [IF ANY]

