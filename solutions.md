## Solution notes

### Task 01 – Run‑Length Encoder

- Language: Go
- Approach:

Create a run-length encoding Encoder method as following

1. Extracting string to character (rune in Go) that make us deal with **unicode** if it's represent as an **emoji**, if it's blank **""** return **""**
2. Iterate it over and count the characters(runes) that are the same in rows
3. Append it next as a unique character by using a builder package in Go and convert count (as int) to string using **strconv.Itoa**

- Why:

1. By extracting a string as a rune we can deal it with emoji as a test results we have an **emoji combine with string**
2. We can append an int count to a string by using **strconv.Itoa**

- Time spent: ~12 min
- AI tools used: Clade AI

### Task 02 – Fix‑the‑Bug

- Language: Go
- Approach:

As it's a problem with race condition where we face a problem by using a goroutine do a task that run as a background and make it unsyncronized.

So I'm using a **Mutex (Lock, Unlock)** in Go to make it as a syncronized operation before we do an operation.

- Why:

By using **Mutex.Lock()** and **Mutex.Unlock()** we can make an operation syncronized. It's only allow one goroutine to do an operation at a time and solve the race condition problem.

- Time spent: ~25 min
- AI tools used: Clade AI
