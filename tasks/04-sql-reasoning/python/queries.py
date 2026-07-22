# tasks/04‑sql‑reasoning/python/queries.py
from pathlib import Path

# --- path to donations.db --------------------------------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "donations.db"

# --- Task A ---------------------------------------------------------------
SQL_A = """
SELECT 
    c.id AS campaign_id,
    COALESCE(SUM(p.amount_thb), 0) AS total_thb,
    ROUND(CAST(COALESCE(SUM(p.amount_thb), 0) AS REAL) / c.target_thb, 4) AS pct_of_target
FROM campaign c
LEFT JOIN pledge p ON c.id = p.campaign_id
GROUP BY c.id, c.target_thb
ORDER BY pct_of_target DESC, campaign_id ASC;
"""

# --- Task B ---------------------------------------------------------------
SQL_B = """
WITH ranked_global AS (
    SELECT 
        amount_thb,
        ROW_NUMBER() OVER (ORDER BY amount_thb ASC) AS rn,
        COUNT(*) OVER () AS total_count
    FROM pledge
),
global_p90 AS (
    SELECT amount_thb AS p90_thb
    FROM ranked_global
    WHERE rn = CAST(ROUND(0.9 * total_count + 0.499999999999999) AS INT) -- จำลอง ceil(0.9 * N)
    -- หรือกรณี SQLite เวอร์ชันใหม่ สามารถใช้ (0.9 * total_count + 0.9999999)
    -- หรือใช้สูตร WHERE rn = CAST(ROUND(CAST(0.9 * total_count AS REAL) + 0.499999) AS INT)
    LIMIT 1
),
ranked_thailand AS (
    SELECT 
        p.amount_thb,
        ROW_NUMBER() OVER (ORDER BY p.amount_thb ASC) AS rn,
        COUNT(*) OVER () AS total_count
    FROM pledge p
    JOIN donor d ON p.donor_id = d.id
    WHERE d.country = 'Thailand'
),
thailand_p90 AS (
    SELECT amount_thb AS p90_thb
    FROM ranked_thailand
    WHERE rn = CAST(ROUND(0.9 * total_count + 0.499999999999999) AS INT)
    LIMIT 1
)
SELECT 'global' AS scope, p90_thb FROM global_p90
UNION ALL
SELECT 'thailand' AS scope, p90_thb FROM thailand_p90;
"""

# --- (skipped) indexes -----------------------------------------------------
INDEXES: list[str] = []        # left empty on purpose

# "CREATE INDEX idx_pledge_campaign_amount ON pledge(campaign_id, amount_thb);",
# "CREATE INDEX idx_donor_country ON donor(country);",