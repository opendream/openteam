## Solution notes - Siwach Toprasert

### Task 01 – Run‑Length Encoder

- Language: Go, C#
- Approach: The algorithm starts by checking for an empty string and returns an empty result if so. It then loops through each character, tracking the current character and its count—adding the character and count to the result when a different one is found—before finally appending the last group after the loop ends.
- Why:
  - String builder is used in both Go and C# to concatinate the final string output.
  - `rune` is used in Go while `StringInfo` is used in C#. This is because of Unicode Safety.
  - Some characters such as `emojis` (`🦄`, etc.) or special character like `é` consist of multiple code units and without proper handling this can cause the encoder to bug and could potentially lead to incorrect encoding.
  - Although `char` can be used in C# and `byte` can be used in Go for much faster and simpler implementation, it is only beneficial for ASCII-only data, meaning that it will not work with emojis or special characters.
  - Lastly, it is easier to maintain unicode-safe approach since it avoids any edge case that could possibly occurs, leading to a much more reliable code long term.
- Time spent: ~10 min
- AI tools used: ChatGPT, Github Copilot

### Task 02 – Fix‑the‑Bug

- Language: Go, C#
- Approach: In both Go and C#, a shared variable (current or \_current) is accessed and modified from multiple threads/goroutines without synchronization. To ensure unique IDs and prevent race conditions, `atomic` is used.
- Why: Atomic operations are actions that occur completely and without interruption, meaning no other thread can observe or interfere while the operation is taking place. When a thread performs an atomic operation, it finishes entirely before any other thread can access the shared data. Another way to manage concurrent access is by using locks, which ensure that only one thread at a time can access or modify a shared resource. However, locking is generally slower due to the overhead of managing thread coordination. Locking is more appropriate for complex or multi-step operations that require consistency across multiple actions. Atomic operations, on the other hand, are ideal for simple, single-step tasks. In this scenario, since the operation only involves a basic counter increment, using an atomic operation is the preferred and more efficient solution.
- Time spent: ~5 min
- AI tools used: ChatGPT

### Task 03 – Sync Aggregator

- Language: C#
- Approach: The method begins by reading a list of file paths from `fileList.txt`. It then initializes a fixed number of worker threads (default is 4) to process each file concurrently. These threads consume jobs from a `BlockingCollection`, which ensures thread-safe and ordered access to the work queue. Each file is processed with a per-file timeout using `Thread.Join()`, and any file that exceeds the timeout is marked with a `"timeout"` status. To ensure that the program waits until all files are processed, a `CountdownEvent` is used. Finally, the results are returned in the same order as the input list by pre-allocating an array and storing each result at its corresponding index.
- Why:
  - `BlockingCollection` ensures thread-safe job queuing and blocking consumption for worker threads.
  - `Thread.Join(timeout)` enables fine-grained per-file timeout control, and `Thread.Interrupt()` cancels overrun operations.
  - `CountdownEvent` is used instead of `Task.WhenAll` or `Thread.Join()` loops to wait for completion efficiently and safely across multiple threads.
  - Using `ThreadPriority.Highest` and `Thread.Yield()` helps reduce scheduling delays during timeout-sensitive operations.
  - This low-level thread management is preferred in this context to fully control timeout behavior, which is harder to do with Task-based APIs in scenarios that require hard interrupts.
  - `Thread` was chosen over `Task/async-await` to enable direct control over thread interruption, which is not easily achievable with tasks.
  - Grace time of 250ms added to avoid false timeouts for borderline timing cases (e.g., `#sleep=2`).
  - Preserving input order was critical; hence, results are indexed and stored accordingly, unlike naive parallel processing which could jumble outputs.
- Time spent: ~60 min
- AI tools used: ChatGPT

### Task 04 – SQL Reasoning

- Language: C#
- Approach:
  - Task A computes the total amount pledged per campaign along with how much of the campaign's target has been raised. A `LEFT JOIN` ensures that campaigns with no pledges are still included. Grouping is done by campaign ID, and the result is ordered by percentage of target achieved (descending), then campaign ID (ascending).
  - Task B calculates the **90th percentile** pledge amount using the **nearest-rank** method. This is done twice: once across all pledges ("global") and once only for pledges from donors in Thailand ("thailand"). For each scope, the query uses a `ROW_NUMBER()` window function to rank pledge amounts, and `COUNT(*) OVER ()` to calculate the total number of pledges. The result at the position `CEIL(0.9 _ total)` is selected.
  - Indexes are added to optimize query performance: one for the campaign ID used in Task A’s JOIN/grouping, and another for the donor ID and amount used in Task B’s JOIN and ORDER BY clauses
- Why:
  - `LEFT JOIN` in Task A ensures inclusion of campaigns with zero pledges, which a standard `INNER JOIN` would exclude.
  - `COALESCE()` is used to safely handle nulls from left joins and ensure `0` is used in sum calculations when no pledges exist.
  - The `ROUND(..., 4)` function satisfies the requirement to round `pct_of_target` to four decimal places.
  - The **nearest-rank percentile** method is used instead of statistical functions like `PERCENTILE_CONT()` (which SQLite doesn't support natively), providing exact results via row numbering.
  - Window functions like `ROW_NUMBER()` and `COUNT(*) OVER ()` are supported in modern SQLite and allow precise percentile logic.
  - The global vs. Thailand breakdown is efficiently handled using two CTEs (`WITH` clauses) and a `UNION ALL` to combine the results in the correct order.
  - Index `idx_pledge_campaign_id` improves JOIN and aggregation performance in Task A.
  - Composite index `idx_pledge_donor_id_amount` accelerates the JOIN with donor and the ORDER BY amount for percentile computation in Task B, ensuring that both filtering and ordering benefit from the index.
- Time spent: ~80 min
- AI tools used: ChatGPT
