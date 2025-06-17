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
- **Approach**: Single worker pool design with `ThreadPoolExecutor` handling multiple files simultaneously, combined with individual timeout control using background threads that can be safely abandoned when files take too long. Results collected using `index mapping` to maintain exact input order despite files completing at different times
- **Why**: The straightforward single-pool architecture avoids complex nested threading issues while providing reliable timeout enforcement. Index-based result ordering ensures output matches input sequence perfectly, achieving both correctness and significant performance gains over sequential processing.
- **Time spent**: ~60 min

## Task 04 – SQL Reasoning
- **Language**: Python
- **Approach**: Built structured database queries using `Common Table Expression (CTE)` calculations for complex percentile analysis, combined data from multiple tables through joins, and created targeted database indexes to speed up the most demanding operations. Organized all SQL queries as standalone constants for clear code structure
- **Why**: `CTE` queries makes complex calculations like percentiles easier to understand and maintain, while indexing on key columns significantly improves query performance for joins and sorting operations. Keeping SQL logic separate from Python code allows for independent testing and easier modifications
- **Time spent**: ~60 min

## Summary

The complete solutions took approximately 2 hours 14 minutes of core development time across all Python tasks (excluding revision, documentation, and break time). The problem-solving approach focused on understanding each task's fundamental challenge before building solutions that prioritized both reliability and performance. Edge cases such as empty strings, single characters, complex Unicode sequences and boundary conditions for run-length encoding were considered but chose the simpler yet effective approach.

Throughout all implementations, I maintained high code quality by applying Python best practices including proper error handling, clean imports, and readable formatting. All original test suites passed without modification, ensuring solutions met exact specifications while maintaining performance

The most technically challenging aspect was the file aggregator, which required careful coordination of multiple threads with timeout handling while preserving exact result ordering. This showcased key technical skills including effective threading patterns, database query optimization, proper Unicode text handling, and efficient algorithm design. GitHub Copilot was used extensively throughout for code assistance, documentation writing, and implementation guidance across all tasks.