# Task 2 – Fix‑the‑Bug (thread‑safe ID generator)

This challenge tests your ability to identify and fix race conditions in concurrent code. The repository contains implementations with **ID generators that are *not* thread‑safe**. Under concurrent load, the current implementations return duplicate values; the unit test suites demonstrate the failure. Your mission is to patch that race condition with *minimal* code.

---

## 1 · Folder Structure

```
tasks/02-fix-the-bug/
├─ python/
│   ├─ buggy_counter.py       # ←‑‑‑ implement thread-safe counter
│   └─ test_counter.py        # failing tests
├─ go/
│   ├─ go.mod                 # Go module file
│   ├─ buggy_counter.go       # implement thread-safe counter
│   └─ buggy_counter_test.go  # failing tests
└─ csharp/
    ├─ BuggyCounter.sln       # solution file
    ├─ BuggyLib/              # class library –‑‑‑‑‑> ❌ buggy code
    │   ├─ BuggyCounter.cs    # ← edit *this* file only
    │   └─ BuggyLib.csproj
    └─ BuggyLib.Tests/        # xUnit tests –‑‑‑‑‑> ✅ do NOT change
        ├─ BuggyCounterTests.cs # exercises heavy parallelism
        └─ BuggyLib.Tests.csproj
```

Pick **one** language and edit only the implementation file.
The tests in that folder will remain red until your fix is correct.

---

## 2 · Specification

### Background

```csharp
// simplified excerpt from BuggyCounter.cs
static long _current = 0;

public static long NextId()
{
    long value = _current;             // two threads may read the same value
    Thread.Sleep(0);                   // exaggerates the race
    _current++;                        // non‑atomic increment
    return value;
}
```

The test `NextId_Should_Not_Duplicate` launches thousands of parallel calls and
asserts that the returned IDs are **unique**.
Today the test fails with a message like:

```
Expected: 0  (duplicates)
Actual:   17
```

---

## 3 · Your job

> 💡 **Start here:** Run the tests first—the failure output shows exactly what's going wrong.

| # | What you must do                                                                                                                      | Where                      |
| - | ------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| 1 | **Do *not* touch the tests.** They define the required behaviour.                                                                     | Test files                 |
| 2 | Apply **one small patch** that makes the ID generator safe for unlimited concurrency.                                                | Implementation files       |
| 3 | Add *≤ 5* comment lines **at the very top of that file** explaining<br>• **why** the race occurred<br>• **how** your fix prevents it. | same file                  |
| 4 | Confirm success by running the tests                                                                                                 | See commands below         |

A passing run should show all tests passing.

---

## 4 · Running the tests locally

```bash
cd tasks/02-fix-the-bug

# Python
python -m pytest python/test_counter.py

# Go
go test ./go

# C#
dotnet test ./csharp
```

All suites assert that the ID generator produces unique values under heavy concurrent load.

Tests pass ✅ only when your implementation is thread-safe.

---

## 5 · Constraints & rules

* **Public API compatibility:** keep the public surface unchanged.
* **Performance:** aim for an O(1), allocation‑free solution (e.g. atomic operations or small lock blocks).
  Elaborate lock‑free algorithms are **not** required.
* **Scope of change:** modify **only** the implementation files. Any edits to project files or tests will be rejected.

---

## 6 · Estimated time

A developer familiar with basic concurrency concepts should finish in **10–15 minutes** including test runs.
Take longer if you need it—understanding thread safety is more important than speed.

Good luck — turn the repo **green**!