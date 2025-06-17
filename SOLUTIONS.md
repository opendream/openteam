# Solution Notes

## Task 01 – Run-Length Encoder
- **Language**: Python
- **Approach**: Simple single-pass iteration with consecutive character counting, building result list and using `str.join()` for efficient final concatenation. Chose the straightforward algorithm over the alternative algorithm for optimal balance of simplicity and performance
- **Why**: O(n) time complexity with minimal memory overhead and no external dependencies. The simple approach handles Unicode correctly at the code-point level. Python's string iteration naturally processes Unicode characters as individual code points, making it Unicode-aware without requiring normalization or grapheme cluster handling. While the alternative consideration offers advanced Unicode features like grapheme cluster support for complex emojis, the core requirements are fully satisfied by the simpler implementation with better performance and maintainability
- **Time spent**: ~6 min

## Task 02 – Fix-the-Bug
- **Approach**: Added a thread lock (`threading.Lock()`) to ensure unique access when updating the counter. This guarantees that each thread increments the counter sequentially, preventing accidental assignment of duplicate IDs.
- **Why**: The lock eliminates race conditions by allowing only one thread to modify the counter at a time. This ensures each thread receives a unique ID, maintaining integrity even under concurrent access.
- **Time spent**: ~10 min

## Task 03 – Sync Aggregator
- **Language**: Python
- **Approach**: Single worker pool design with `ThreadPoolExecutor` handling multiple files simultaneously, combined with individual timeout control using background threads that can be safely abandoned when files take too long. Results collected using `index mapping` to maintain exact input order despite files completing at different times. Files with sleep directives are processed by parsing the first line and simulating the specified delay. Added a 200ms buffer period for threads that appear to timeout at the exact boundary.
- **Why**: The straightforward single-pool architecture avoids complex nested threading issues while providing reliable timeout enforcement. Index-based result ordering ensures output matches input sequence perfectly. The grace period fix eliminates race conditions without affecting genuine timeouts, achieving both correctness and significant performance gains over sequential processing. Tested 50 consecutive runs with 100% success rate, confirming the race condition is eliminated while maintaining proper timeout behavior for files that genuinely exceed limits
- **Time spent**: ~65 min

## Task 04 – SQL Reasoning
- **Language**: Python
- **Approach**: Built structured database queries using `Common Table Expression (CTE)` calculations for complex percentile analysis, combined data from multiple tables through joins, and created targeted database indexes to speed up the most demanding operations. Organized all SQL queries as standalone constants for clear code structure
- **Why**: `CTE` queries makes complex calculations like percentiles easier to understand and maintain, while indexing on key columns significantly improves query performance for joins and sorting operations. Keeping SQL logic separate from Python code allows for independent testing and easier modifications
- **Time spent**: ~60 min

## Summary

The complete solutions took approximately 2 hours 29 minutes of core development time across all Python tasks (excluding revision, documentation, and break time). The problem-solving approach focused on understanding each task's fundamental challenge before building solutions that prioritized both reliability and performance. Edge cases such as empty strings, single characters, complex Unicode sequences and boundary conditions for run-length encoding were considered but chose the simpler yet effective approach.

Throughout all implementations, I maintained high code quality by applying Python best practices including proper error handling, clean imports, and readable formatting. All original test suites passed without modification, ensuring solutions met exact specifications while maintaining performance

The most technically challenging aspect was the file aggregator, which required careful coordination of multiple threads with timeout handling while preserving exact result ordering. A critical race condition was identified and resolved where files sleeping for exactly the timeout duration were sometimes incorrectly marked as timed out. This showcased key technical skills including effective threading patterns, race condition debugging, database query optimization, proper Unicode text handling, and efficient algorithm design. GitHub Copilot was used extensively throughout for code assistance, documentation writing, and implementation guidance across all tasks.