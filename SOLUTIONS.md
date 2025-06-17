# Solution Notes

## Task 1 – Run-Length Encoder

- **How you solved it**  
  I implement a Run Length Encoding algorithm that iterate through the input string tracking the current character and its consecutive count.

- **Why this approach**  
  This approach is optimal of performance and simple. It achieves O(n) time complexity by processing the string in one pass.

- **Time spent**  
  About 20 minutes for Solve the problem.

---

## Task 2 – Fix-the-Bug (Thread-Safe ID Generator)

- **How you solved it**  
  I fix the race condition by introducing a threading.Lock to protect the critical section where the shared counter.

- **Why this approach**  
  Using a threading.Lock is the standard approach in Python for ensuring thread safety.

- **Time spent**  
  About 10 minutes for Solve the problem.
