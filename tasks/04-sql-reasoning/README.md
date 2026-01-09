# Task 4 – SQL Reasoning (Data analytics & index design)

This advanced challenge tests your ability to write efficient SQL queries and design indexes for performance optimization. You'll work with a realistic donations database and need to produce exact results while ensuring optimal query execution.

---

## 1 · Folder Structure

```
tasks/04-sql-reasoning/
├─ donations.db              # SQLite 3.45 database (≈ 50k pledges)
├─ schema.sql                # Reference DDL (read‑only)
├─ expected/                 # Ground‑truth produced by our reference solution
│   ├─ q1.csv
│   └─ q2.csv
├─ python/
│   ├─ queries.py            # ←‑‑‑ fill SQL_A, SQL_B, INDEXES
│   └─ test_queries.py       # failing tests
├─ go/
│   ├─ go.mod                # Go module file
│   ├─ queries.go            # implement SQL constants
│   └─ queries_test.go       # failing tests
└─ csharp/
    ├─ Queries.cs            # implement SQL constants
    ├─ QueriesTests.cs       # failing tests
    └─ SqlReasoning.csproj   # C# project file
```

Pick **one** language and edit only the implementation file.
The tests in that folder will remain red until your queries are correct.

---

## 2 · Specification

### Database schema

```sql
campaign (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    target_thb   INTEGER NOT NULL CHECK(target_thb > 0),
    owner_id     INTEGER,
    created_at   TEXT  -- ISO‑8601 date string
)

donor (
    id       INTEGER PRIMARY KEY,
    email    TEXT NOT NULL,
    country  TEXT NOT NULL            -- ISO‑3166 English short name
)

pledge (
    id           INTEGER PRIMARY KEY,
    donor_id     INTEGER NOT NULL REFERENCES donor(id),
    campaign_id  INTEGER NOT NULL REFERENCES campaign(id),
    amount_thb   INTEGER NOT NULL,
    pledged_at   TEXT    -- ISO‑8601 date string
)
```

### Task A – Total raised per campaign

Return **one row per campaign** with:

| column          | type | description                                   |
| --------------- | ---- | --------------------------------------------- |
| `campaign_id`   | INT  | `campaign.id`                                 |
| `total_thb`     | INT  | sum of all pledges for that campaign          |
| `pct_of_target` | REAL | `total_thb / target_thb`, **rounded to 4 dp** |

*Order the result by* **`pct_of_target` descending, then `campaign_id` ascending**.

### Task B – 90‑percentile pledge amount

Produce **exactly two rows**:

| column    | type | value                         | notes                           |
| --------- | ---- | ----------------------------- | ------------------------------- |
| `scope`   | TEXT | `'global'` \| `'thailand'`    | output in this order            |
| `p90_thb` | INT  | 90‑percentile of `amount_thb` | nearest‑rank method (see below) |

*Nearest‑rank rule*:
If a set contains *N* rows ordered ascending by `amount_thb`, the 90‑percentile is the value at rank `ceil(0.9 × N)` (1‑based).

The `thailand` row uses only pledges whose donor's `country = 'Thailand'` (case‑sensitive).

### Task C – Index optimization

Return **exactly two `CREATE INDEX …` statements**:

1. First index must make Task A faster.
2. Second index must make Task B faster.

Tests verify that **each query performs at least one indexed search** (no full‑table scans).

---

## 3 · Your job

> 🔧 **Explore the database first:**
> ```bash
> sqlite3 tasks/04-sql-reasoning/donations.db
> .schema          -- see table structure
> .mode column     -- readable output
> SELECT * FROM pledge LIMIT 5;
> SELECT * FROM campaign LIMIT 5;
> SELECT * FROM donor LIMIT 5;
> ```

| File                                       | Constant  | Expected value                                     |
| ------------------------------------------ | --------- | -------------------------------------------------- |
| `queries.py` / `queries.go` / `Queries.cs` | `SQL_A`   | your SELECT for Task A                             |
|                                            | `SQL_B`   | your SELECT for Task B                             |
|                                            | `INDEXES` | iterable with exactly two `CREATE INDEX …` strings |

**Do not** edit test files or modify the database schema.

---

## 4 · Running the tests locally

```bash
cd tasks/04-sql-reasoning

# Python
pytest python/test_queries.py

# Go
go test ./go

# C#
dotnet test ./csharp
```

Each test suite:

1. Opens *donations.db* in read‑only mode.
2. Creates your indexes (if any).
3. Executes `SQL_A` → compares against `expected/q1.csv`.
4. Executes `SQL_B` → compares against `expected/q2.csv`.
5. Verifies both query plans include at least one `SEARCH TABLE … USING INDEX`.

Tests pass ✅ only when your queries produce exact results and use efficient execution plans.

---

## 5 · Estimated time

A senior engineer fluent in SQL window functions and index design should finish in **45–60 minutes** including test runs.
This task requires deep understanding of SQL analytics functions and performance optimization.

Take your time—precision and optimization are key skills for senior developers.

Good luck 🎯