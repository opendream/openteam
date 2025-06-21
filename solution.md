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