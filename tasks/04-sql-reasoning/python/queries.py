# tasks/04‑sql‑reasoning/python/queries.py
from pathlib import Path

# --- path to donations.db --------------------------------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "donations.db"

# --- Task A ---------------------------------------------------------------
SQL_A = """
SELECT
    c.id AS campaign_id,
    SUM(p.amount_thb) AS total_thb,
    ROUND(SUM(p.amount_thb) * 1.0 / c.target_thb, 4) AS pct_of_target
FROM campaign c
JOIN pledge p ON p.campaign_id = c.id
GROUP BY c.id, c.target_thb
ORDER BY pct_of_target DESC, total_thb DESC, c.id ASC
LIMIT 10;
"""

# --- Task B ---------------------------------------------------------------
SQL_B = """
WITH global_pledges AS (
    SELECT amount_thb FROM pledge ORDER BY amount_thb
),
global_count AS (
    SELECT COUNT(*) AS cnt FROM global_pledges
),
global_p90 AS (
    SELECT 'global' AS scope, CAST((SELECT amount_thb FROM global_pledges LIMIT 1 OFFSET (SELECT CAST(ROUND(0.9 * (cnt-1)) AS INT) FROM global_count)) AS INT) AS p90_thb
),
th_pledges AS (
    SELECT p.amount_thb FROM pledge p JOIN donor d ON p.donor_id = d.id WHERE d.country = 'Thailand' ORDER BY p.amount_thb
),
th_count AS (
    SELECT COUNT(*) AS cnt FROM th_pledges
),
th_p90 AS (
    SELECT 'thailand' AS scope, CAST((SELECT amount_thb FROM th_pledges LIMIT 1 OFFSET (SELECT CAST(ROUND(0.9 * (cnt-1)) AS INT) FROM th_count)) AS INT) AS p90_thb
)
SELECT * FROM global_p90
UNION ALL
SELECT * FROM th_p90;
"""

INDEXES: list[str] = [
    "CREATE INDEX idx_pledge_campaign_id ON pledge(campaign_id);",
    "CREATE INDEX idx_pledge_amount_thb ON pledge(amount_thb);",
]
