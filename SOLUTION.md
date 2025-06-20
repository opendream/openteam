## Solution notes

### Task 01 – Run‑Length Encoder
- **Languages**: Go, Python
- **Approach**:
  - For **Go**, I converted the input string to a `[]rune` slice to handle Unicode characters (e.g., emojis), then iterated through each character while counting consecutive duplicates. I used a `strings.Builder` for efficient string concatenation.
  - For **Python**, I used a loop to iterate over the string while tracking the current character and its count, appending the character and count to a result list. The final result is joined into a string.
- **Why**: Both implementations ensure:
  - Case-sensitivity
  - Multi-digit support (e.g., `C12`)
  - Full Unicode compatibility
  - Linear time complexity O(n)
- **Time spent**: ~12 minutes
- **AI tools used**: ChatGPT 

---

### Task 02 – Fix‑the‑Bug (Thread Safety)
- **Languages**: Go, Python
- **Approach**:
  - For **Go**, I used a `sync.Mutex` to lock access to the shared counter (`current`) in the `NextID()` function. This prevents race conditions by ensuring only one goroutine can read and increment the counter at a time.
  - For **Python**, I used a `threading.Lock()` to wrap the global counter increment. This avoids the read-modify-write race under concurrent access.
- **Why**: The original code had a race condition where multiple threads or goroutines could read the same value before incrementing, causing duplicate IDs. Using a lock (mutex) ensures atomicity of the increment operation, fixing the bug without altering the intended logic.
- **Time spent**: ~8 minutes
- **AI tools used**: ChatGPT

---

## Notes
- All test files were kept unchanged.
- All tests pass locally using `pytest` for Python and `go test` for Go.
- Languages used: Go 1.24.4, Python 3.9.6 (on macOS)
- `.zshrc` and PATH were updated to make `pytest` accessible from `~/.local/bin`