# tasks/04‑sql‑reasoning/python/queries.py
from pathlib import Path

# --- path to donations.db --------------------------------------------------
DB_PATH = Path(__file__).resolve().parent.parent / "donations.db"

# --- Task A ---------------------------------------------------------------
# Total raised per campaign with percentage of target
SQL_A = """
SELECT 
    c.id AS campaign_id,
    COALESCE(SUM(p.amount_thb), 0) AS total_thb,
    ROUND(CAST(COALESCE(SUM(p.amount_thb), 0) AS REAL) / c.target_thb, 4) AS pct_of_target
FROM campaign c
LEFT JOIN pledge p ON c.id = p.campaign_id
GROUP BY c.id, c.target_thb
ORDER BY pct_of_target DESC, campaign_id ASC
"""

# --- Task B ---------------------------------------------------------------
# 90th percentile pledge amounts for global and Thailand
SQL_B = """
WITH ranked_pledges AS (
    SELECT 
        p.amount_thb,
        d.country,
        ROW_NUMBER() OVER (ORDER BY p.amount_thb ASC) AS global_rank,
        COUNT(*) OVER () AS global_count,
        ROW_NUMBER() OVER (
            PARTITION BY CASE WHEN d.country = 'Thailand' THEN 1 ELSE 0 END 
            ORDER BY p.amount_thb ASC
        ) AS thailand_rank,
        COUNT(*) OVER (
            PARTITION BY CASE WHEN d.country = 'Thailand' THEN 1 ELSE 0 END
        ) AS thailand_count
    FROM pledge p
    JOIN donor d ON p.donor_id = d.id
),
global_p90 AS (
    SELECT amount_thb AS p90_thb
    FROM ranked_pledges
    WHERE global_rank = CAST(CEILING(0.9 * global_count) AS INTEGER)
    LIMIT 1
),
thailand_p90 AS (
    SELECT amount_thb AS p90_thb
    FROM ranked_pledges
    WHERE country = 'Thailand' 
    AND thailand_rank = CAST(CEILING(0.9 * thailand_count) AS INTEGER)
    LIMIT 1
)
SELECT 'global' AS scope, p90_thb FROM global_p90
UNION ALL
SELECT 'thailand' AS scope, p90_thb FROM thailand_p90
"""

# --- (skipped) indexes -----------------------------------------------------
INDEXES: list[str] = [
    "CREATE INDEX idx_pledge_campaign_id ON pledge(campaign_id)",
    "CREATE INDEX idx_pledge_donor_id ON pledge(donor_id)"
]
