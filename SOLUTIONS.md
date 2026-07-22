## Solution notes

### Task 01 – Run‑Length Encoder
- Language: python
- Approach: Seperate string to list of characters and loop count.
- Why: simplicity
- Time spent: ~10 min
- AI tools used: Gemini

### Task 02 – Fix‑the‑Bug
- Language: Python
- Approach: Use threading.Lock so that other threads can't read or update _current at the same time.
- Why: simplicity
- Time spent: ~ 15 min
- AI tools used: Gemini

### Task 03 – Sync-Aggregator
- Language: Python
- Approach: Use ThreadPoolExecutor with micro-polling sleep (0.02s increments) to enforce strict timeouts instantly without blocking threads, ensuring exact file-list order and execution time well under 6 seconds.
- Why: simplicity
- Time spent: ~ 40 min
- AI tools used: Gemini

### Task 04 – SQL-Reasoning
- Language: Python
- Approach: 
    Task A (SQL_A): Use a LEFT JOIN between campaign and pledge grouped by campaign ID, aggregating total pledges with COALESCE and calculating pct_of_target via ROUND(SUM(amount_thb) / target_thb, 4).
    Task B (SQL_B): Use Common Table Expressions (CTEs) with window functions (ROW_NUMBER() and COUNT(*)) to sort pledge amounts, filtering the exact 90th percentile rank using ceil(0.9 * N) for both global and Thailand scopes before combining them with UNION ALL.
- Why: simplicity
- Time spent: ~ 15 min
- AI tools used: Gemini