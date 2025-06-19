## Solution notes

### Task 01 – Run‑Length Encoder
- Language: csharp
- Approach: Use loop to check each chareacter. For each character, If it's the same as the previous character,it will increment a count. Otherwise, f different, append the previous character and count to a result builder, then reset the count. Lastly, append the final character and count.

- Why: using char.IsHighSurrogate / IsLowSurrogate to handel unicode safely becasue some special characters have a Unicode code higher than U+FFFF, so .NET uses 2 chars instead of 1 letter. Uses StringBuilder (standard .NET library) for fast string concatenation

- Time spent: ~12 min
- AI tools used: ChatGPT, I use to find How to check emoji and store emoji

### Task 02 – Fix‑the‑Bug
- Language: csharp
- Approach: Replace Thread.Sleep(0) with Interlocked.Increment() method
- Why: because Interlocked.Increment method ensures that increment + return is done as a single atomic operation across threads, and Thread.Sleep(0) is not garuntee to next context
- Time spent: ~8 min
- AI tools used: ChatGPT,
