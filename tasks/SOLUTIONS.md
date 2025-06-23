# Solution Notes

## Task 01 - Run-Length Encoder

- Language: Python
- Approach: Single-pass algorithm that tracks current character and count, appending `{current_char}{count}` groups to a result list when characters change, then joins once at the end.
- Why: O(n) time/space complexity as required. Using list + join avoids quadratic string concatenation. Python's string iteration naturally handles Unicode code points correctly for emoji support.
- Time spent: ~5 min

## Task 02 - Fix-the-Bug

- Language: Python  
- Approach: Added `threading.Lock()` and wrapped the read-increment-return sequence in a `with _lock:` context manager to make the critical section atomic.
- Why: The race condition occurred because multiple threads could read the same `_current` value before any incremented it. The lock ensures only one thread executes the critical section at a time, eliminating interleaving operations. Lock-based solution prioritizes simplicity and correctness over maximum performance but might introduces serialization bottleneck but ensures thread safety. And used context manager for automatic lock release on exceptions.
- Time spent: ~10 min

## Task 03 - Sync Aggregator

- Language: Python
- Approach: Used `ThreadPoolExecutor` with worker pool, submitted all file processing tasks concurrently, enforced per-file timeouts with `future.result(timeout=timeout)`, and preserved result order using index mapping. Handled `#sleep=N` markers by parsing and removing them before line/word counting.
- Why: ThreadPoolExecutor provides clean concurrency with timeout support. Pre-allocated results array with future-to-index mapping maintains input order despite concurrent execution. Thread-based parallelism chosen over multiprocessing for simpler shared state and lower overhead, though CPU-bound workloads might benefit from processes. Pre-allocated results array uses extra memory but guarantees order preservation. Future-to-index mapping adds complexity but eliminates need for result sorting. Alternative async/await approach would be more scalable but requires different timeout handling patterns.
- Time spent: ~60 min (including debugging timeout logic and file path resolution)

## Task 04 - SQL Reasoning

- Language: Python (SQLite)
- Approach:
  - Task A: LEFT JOIN campaign+pledge tables, SUM amounts with COALESCE for zero-pledge campaigns, calculate percentage as `CAST(total AS REAL) / target` with ROUND to 4dp
  - Task B: Used window functions with ROW_NUMBER() to implement nearest-rank percentile method (`CEILING(0.9 * N)`), separate calculations for global vs thailand scope
  - Task C: Created indexes on foreign key columns (`pledge.campaign_id`, `pledge.donor_id`) to optimize JOIN operations
- Why: LEFT JOIN ensures all campaigns appear even with zero pledges. CAST to REAL prevents integer division truncation. Window functions provide precise percentile calculation per nearest-rank specification. Foreign key indexes eliminate full table scans on JOIN operations. CTEs prioritize readability over raw performance. It might be more memory usage but easier debugging and maintenance. Index on foreign keys improves JOIN performance but increases storage overhead and insert/update costs. Window functions vs subquery approaches trade complexity for SQL standard compliance and optimizer efficiency.
- Time spent: ~45 min

## Overall

- AI Assistance: Used Claude AI for implementation guidance, algorithm design and debugging assistance
- Time vs Estimates: Generally aligned with provided estimates though Task 3 took longer due to concurrency debugging
- Key Skills Exercised: Concurrent programming, SQL analytics, algorithm optimization, thread safety, performance tuning
