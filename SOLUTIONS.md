# SOLUTIONS.md

- **Candidate:** Aung Khant Phyo
- **Time spent:** ~ 83 min


## Task 01 – Run‑Length Encoder

- **Language:** Python
- **Approach:** I implemented a single for loop. In each iteration, check whether the index char is the same as the next nearest char. If yes, count for this char up, and if not, the char and its count is appended to the result list. At the end of the loop, I append the last char and its counter, and print out the list with no-space joining.
- **Why this approach:** Uaing a single loop make sure achieveing linear pattern in Big O notation. In this case, the program's time complexity is O(N).
- **Time spent:** ~ 10 min
- **Edge cases considered:** Empty input.
- **AI tools used:** None


## Task 02 – Fix‑the‑Bug (Thread Safety)

- **Language:** Python
- **Approach:** Replaced unsafe increment logic with a thread-safe operation using a locking mechanism (with statement and threading.Lock).
- **Why this approach:** Using a lock ensures that only one thread can access and modify the shared global variable at a time, which prevents race conditions.
- **Time spent:** ~ 3 min
- **AI tools used:** None


## Task 03 – Sync Aggregator (Concurrency & I/O)

- **Language:** Python
- **Approach:** For task 03, my approach was to first read all file paths from the provided file list, ensuring their order is preserved. I then used a thread pool (ThreadPoolExecutor) to process multiple files concurrently, with the number of worker threads set by the input parameter. For each file, I defined a function that opens the file, checks for a sleep directive on the first line, and processes the file by counting lines and words, all while enforcing a strict per-file timeout. If a file exceeds its timeout, the function returns only the path and a timeout status. To maintain the original order, I mapped each task to its file’s index and, after processing, assembled the results in the same sequence as the input. This ensures efficient, concurrent processing with correct timeout handling and output formatting.
- **Why this approach:** I chose multiprocessing over the more lightweight threading approach because true parallelism was required. While threading is effective for I/O-bound tasks, this task involved CPU-bound operations—such as file parsing and processing—where Python's Global Interpreter Lock (GIL) limits the effectiveness of threads. Even OS-level threads cannot bypass the GIL for parallel CPU-bound execution. Additionally, I implemented a custom timeout mechanism instead of relying on ThreadPoolExecutor's built-in timeout, because Python threads cannot be forcibly interrupted during blocking operations like sleep(). By handling timeouts manually at the task level, I ensured better control over how long each file is allowed to run, especially for files with #sleep= directives.

This task gave me deeper insight into Python's concurrency model—particularly the differences between threading and multiprocessing, the limitations imposed by the GIL, and how timeout mechanisms behave with blocking operations. It also helped me understand how to manage concurrency while preserving task order and handling edge cases robustly.

Thank you for the opportunity to work on this task—it was both challenging and educational.

- **Time spent:** ~ 70 min
- **Edge cases considered:**
    - Files with a `#sleep=` directive that exactly matches or slightly exceeds the timeout.
    - Files with no `#sleep=` directive.
    - Files that are empty or contain only whitespace.
    - Files that do not exist or cannot be opened (I/O errors).
    - Files with unusual or invalid `#sleep=` values (e.g., non-integer).
    - Ensuring the result order matches the input file list, even if some files timeout or error.
    - Handling a mix of fast and slow files in the same batch.
    - Very short timeout values (e.g., zero or near-zero).
    - Large file lists with more files than worker threads.
    - Files with non-UTF-8 encodings or unexpected content.
- **AI tools used:** ChatGPT (used to clarify the behavior of ThreadPoolExecutor timeouts, specifically why timeouts do not forcibly interrupt I/O-bound or sleep operations. I also consulted ChatGPT to better understand the per-file timeout requirements, especially regarding test cases 3 and 15, as I am confused when this 2 testcases are not passed as I mentioned in the program.)


## Task 04 – SQL Reasoning (Data Analytics & Index Design)

- **Status:** Not Implemented
- **Reason** Role level did not require it
