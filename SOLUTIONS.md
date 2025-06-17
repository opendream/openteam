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
[] Done 
- Language: Go
- Approach: [EXPLAIN THE FIX]
- Why: [WHY THIS SOLUTION]
- Time spent: ~8 min
- AI tools used: [IF ANY]

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

