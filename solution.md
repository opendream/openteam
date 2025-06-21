## Solution notes

### Task 01 – Run‑Length Encoder
- Language: python
- Approach: I create a count dict first to store each char and its count then concate it later
- Why: I have an experience using this to quickly query the data.
- Time spent: 5 min
- AI tools used: None

### Task 02 – 02-fix-the-bug
- Language: python
- Approach: Using Thread lock instead of sleep(0) for handling multiple thread
- Why: When there is multiple thread that access the same value it can be a race condition which thread.lock can handle that
- Time spent: 8 min
- AI tools used: ChatGPT

### Task 03 – 03-sync-aggregator
- Language: python
- Approach: Using thread executer each thread check each file ft their timeout value is more than setting then quit
- Why: At first i try using real timeout to check and it can't pass the test eventually i use the check each file if their timeout value is more than setting then quit and it finally pass
- Time spent: 56 min
- AI tools used: ChatGPT


### Task 04 – 04-sql-reasoning
- Language: python
- Approach: ---
- Why: I don’t have much experience with SQL yet, so I relied on AI to guide me through correct query.
- Time spent: 40
- AI tools used: ChatGPT